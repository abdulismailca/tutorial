from datetime import date
from email.policy import default

from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError


class MachineTransfer(models.Model):
    _name = 'machine.transfer'
    _description = 'machine transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'machine_selection_id'



    active = fields.Boolean(default=True)
    machine_selection_id = fields.Many2one("machine.management", required=True,
                                           string="Machine")

    company_id = fields.Many2one("res.company",
                                 default=lambda self: self.env.company.id)

    """i use this for filter , like install and service"""
    alternate_ids = fields.Many2many('machine.management',
                                     compute='compute_alternate_ids')

    machine_serial_number = fields.Char(
        related="machine_selection_id.serial_number", string="Serial No")
    transfer_date = fields.Date(string="Transfer Date", default=lambda self: date.today())

    transfer_type = fields.Selection(
        [('install', 'Install'), ('remove', 'Remove')], default='install', string="Transfer Type", required=True)

    customer_id = fields.Many2one("res.partner", string="Customer")

    internal_notes = fields.Text(string="Internal Notes")

    """sequence number field"""
    sequence_number = fields.Char(string="Sequence Number", default='New',
                                  readonly=True, copy=False)

    # the below variable defined only for invisible transfer button &visible ribbon
    is_ribbon_and_button_invisible = fields.Boolean(default=True)

    """sequence number generating"""

    def create(self, vals):

        if vals.get('sequence_number', 'New') == 'New':
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code(
                'machine.transfer')
        return super(MachineTransfer, self).create(vals)


    """machine transfer button function"""
    def machine_transfer(self):
        """if type is install need to asign customer"""
        if self.transfer_type =='install':
            print("iam inside transfer type")
            if not self.customer_id:
                print("inside customer block")
                raise UserError("Please Select a Customer")



        self.machine_selection_id.write({'customer_id': self.customer_id})

        # self.machine_selection_id.state = 'in_service' - we can use below method instead of this

        self.machine_selection_id.write({'state': 'in_service'})

        # self.is_ribbon_and_button_invisible = False - we can use below method instead of this
        self.write({'is_ribbon_and_button_invisible': False})

    @api.depends('transfer_type')
    def compute_alternate_ids(self):
        for rec in self:

            if rec.transfer_type == 'install':

                machines = self.alternate_ids.search(
                    [('state', '=', 'active')])


            elif rec.transfer_type == 'remove':

                machines = self.alternate_ids.search(
                    [('state', '=', 'in_service')])

            else:

                machines = self.alternate_ids.search([])

            # rec.alternate_ids = machines-> instaed of this i use link

            self.update({
                'alternate_ids': [(fields.Command.link(a.id)) for a in machines]
            })
