from datetime import date, timedelta
from email.policy import default
from importlib.resources._common import _

from odoo import api, exceptions, fields, models
from odoo.cli.scaffold import env
from odoo.exceptions import UserError, ValidationError


class MachineModel(models.Model):
    _name = "machine.management"
    _description = "machine management description"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    category_id = fields.Many2one('ir.module.category', string='User Category')

    last_service_date = fields.Date(readonly=True)
    service_frequency = fields.Selection(
        [('monthly', 'Monthly'), ('weekly', 'Weekly'), ('yearly', 'Yearly')],
        default='monthly')
    active = fields.Boolean(default=True)
    name = fields.Char(string="Name", required=True, tracking=True,
                       ondelete="restrict")
    date_of_purchase = fields.Date(string="Date of Purchase", required=True,
                                   tracking=True,
                                   help='When purchased the machine.')

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    purchase_value = fields.Monetary(string="Purchase Value", tracking=True,
                                     help='Amount of purchase.')
    customer_id = fields.Many2one("res.partner", string="Customer Name",
                                  readonly=True, tracking=True,
                                  help='Enter customer name.')
    image = fields.Image()
    description = fields.Text(string="Description", tracking=True)
    machine_instructions = fields.Html(string="Machine Instructions")
    state = fields.Selection(
        [('active', 'Active'), ('in_service', 'In Service')], string="State",
        default="active")
    is_warranty = fields.Boolean(default=True, string="Warranty",
                                 help='Is under warranty- yes/no.')
    serial_number = fields.Char(copy=False, help="Enter the serial number", required=True)

    machine_type = fields.Many2one("machine.types", string="Machine Types")

    sequence_number = fields.Char(string="Sequence Number", default='New',
                                  readonly=True, copy=False)
    company_id = fields.Many2one("res.company",
                                 default=lambda self: self.env.company.id)
    machine_transfer_record_ids = fields.One2many("machine.transfer",
                                                  "machine_selection_id",
                                                  string="Machine transfer record")

    machine_service_record_ids = fields.One2many("machine.service",
                                                 'machine_id',
                                                 string="Machine Service")

    transfer_count = fields.Integer(
        compute="machine_transfer_smart_button_count")
    service_count = fields.Integer(compute="machine_service_smart_button_count")

    machine_tags_ids = fields.Many2many("machine.tags", string="Machine Tags")

    machine_parts_ids = fields.One2many("machine.parts", "machine_name_id",
                                        string="Machine Parts")

    machine_age = fields.Integer(string="Machine Age", default=0,
                                 compute="machine_age_calculation")

    service_recurring_id = fields.Many2one("machine.service",
                                           string="Service Recuring")

    def action_archive(self):
        # super(MachineModel, self).action_archive()

        """"id edha print avunne nne nokkaan ittadhane , but still print 168,169 etc"""
        # print("service id", self.machine_service_record_ids)

        if not self.env.user.has_group('machine_management.group_manager_person'):
            raise UserError('You cannot archive machines')

        for record in self:
            if record.state == 'in_service':
                raise UserError("In service machine can not archive.")

            """archive related customer"""

            record.customer_id.write({'active': False})

            """archive related transfer"""

            self.machine_transfer_record_ids.action_archive()

            """we are checking any service is there in open sate , give warning and canceling below"""

            for record in record.machine_service_record_ids:

                if record.state == 'open':

                    record.write({'state': 'cancel'})
                    record.action_archive()

                    self.active = False
                    return {

                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Warning!',
                            'message': 'Found an open service, we are canceling it!',
                            'type': 'warning',
                            'sticky': False,

                        }
                    }


                else:
                    record.action_archive()

        return super(MachineModel, self).action_archive()

    def action_unarchive(self):

        for record in self:
            """unarchive related customer"""
            record.customer_id.write({'active': True})

            """unarchived related services"""
            service_archive_record = self.machine_service_record_ids.search(
                [
                    ('machine_id', '=', record.id),
                    ('active', '=', False)
                ]
            )
            service_archive_record.write({'active': True})

            """unarchive related transfer"""
            transfer_archive_record = self.machine_transfer_record_ids.search(
                [
                    ('machine_selection_id', '=', record.id),
                    ('active', '=', False)
                ]
            )

            transfer_archive_record.write({'active': True})

        return super(MachineModel, self).action_unarchive()

    """ # purchase value checking is greater than zero."""

    @api.constrains("purchase_value")
    def check_value(self):
        for record in self:
            if record.purchase_value <= 0:
                raise exceptions.UserError("Purchase Value Must be Positive!")

    _sql_constraints = [
        ('serial_number', 'UNIQUE(serial_number)',
         'Serial Number Must be Unique!')
    ]

    """"# sequence_number generating here"""

    def create(self, vals):

        if vals.get('sequence_number', 'New') == 'New':
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code(
                'machine.management')
        return super(MachineModel, self).create(vals)

    """"# redirect to machine transfer"""

    def redirect_to_machine_transfer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine Transfer',
            'res_model': 'machine.transfer',
            'view_mode': 'form',
            'context': {
                'default_machine_selection_id': self.id
            }
        }

    """" # smart button history redirect"""

    def machine_transfer_smart_button_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine Transfer',
            'res_model': 'machine.transfer',
            'view_mode': 'list,form',
            'domain': [('machine_selection_id', '=', self.id)],
        }

    """ # smart button count calculation"""

    def machine_transfer_smart_button_count(self):

        # record.transfer_count = record.len(machine_transfer_record_ids)-instead of this i used below code

        for record in self:
            count_of_record = len(record.machine_transfer_record_ids)
            record.write({'transfer_count': count_of_record})

    """"machine age calculation"""

    @api.depends('date_of_purchase')
    def machine_age_calculation(self):
        today = date.today()

        for record in self:
            if record.date_of_purchase:

                machine_age_calculated = today.year - record.date_of_purchase.year - (
                        (today.month, today.day) < (
                    record.date_of_purchase.month,
                    record.date_of_purchase.day)
                )
                record.write({'machine_age': machine_age_calculated})
                if record.machine_age < 0:
                    record.write({'machine_age': 0})


            else:
                record.write({'machine_age': 0})

    def redirect_to_machine_service(self):
        parts_data = []
        for part in self.machine_parts_ids:
            parts_data.append((0, 0, {
                'machine_parts_id': part.machine_parts_id.id,
                'machine_uom_id': part.machine_uom_id.id,
                'machine_parts_qty': part.machine_parts_qty,
            }))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine Service',
            'res_model': 'machine.service',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_machine_id': self.id,
                'default_customer_id': self.customer_id.id,
                'default_tech_person_id': self.env.user.id,
                'default_machine_service_parts_ids': parts_data,
            }
        }

    """"# machine_service_smart_button_history"""

    def machine_service_smart_button_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine Service',
            'res_model': 'machine.service',
            'view_mode': 'list,form',
            'domain': [('machine_id', '=', self.id)]
        }

    """" #service count"""

    def machine_service_smart_button_count(self):
        for record in self:
            count_of_record = len(record.machine_service_record_ids)
            record.write({'service_count': count_of_record})
