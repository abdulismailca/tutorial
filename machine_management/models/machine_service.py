from datetime import date, timedelta
from email.policy import default
from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class MachineService(models.Model):
    _name = "machine.service"
    _description = "machine service"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'machine_id'

    active = fields.Boolean(default=True)

    machine_id = fields.Many2one("machine.management", string="Machine",
                                 required=True)
    customer_id = fields.Many2one(
        "res.partner", string="Customer",
        required=True,

    )

    date = fields.Date(string="Date", required=True)
    description = fields.Html(string="Description")
    internal_notes = fields.Text(string="Internal Notes")
    tech_person_ids = fields.Many2many('res.users', string='Tech Person')

    state = fields.Selection(
        [('open', 'Open'), ('started', 'Started'), ('done', 'Done'),
         ('cancel', 'Cancel')],
        default='open'
    )

    company_id = fields.Many2one("res.company",
                                 default=lambda self: self.env.company.id)
    machine_service_parts_ids = fields.One2many(
        "machine.parts", "machine_service_parts_id", string="Machine Parts",

    )

    invoice_id = fields.Many2one('account.move', string="Invoice")
    is_invoice_created = fields.Boolean(default=False)
    is_smart_button_visible = fields.Boolean(default=False)
    is_ribbon_paid = fields.Boolean(default=False,
                                    compute="machine_service_paid")

    def action_archive(self):
        if not self.env.user.has_group(
                'machine_management.group_manager_person'):
            raise UserError('You cannot archive service')

        return super(MachineService, self).action_archive()

    def create_recurring_service(self):

        machines = self.machine_id.search([])

        today = date.today()

        for record in machines:

            if record.service_frequency == 'monthly':
                if record.last_service_date:
                    next_recuring_date = record.last_service_date + timedelta(
                        days=30)
                else:
                    next_recuring_date = today + timedelta(
                        days=30)

            elif record.service_frequency == 'weekly':
                if record.last_service_date:
                    next_recuring_date = record.last_service_date + timedelta(
                        days=7)
                else:
                    next_recuring_date = today + timedelta(
                        days=7)
            elif record.service_frequency == 'yearly':
                if record.last_service_date:
                    next_recuring_date = record.last_service_date + timedelta(
                        days=365)
                else:
                    next_recuring_date = today + timedelta(
                        days=365)
            else:
                continue

            if record.state == 'in_service':

                open_service = record.machine_service_record_ids.filtered(
                    lambda s: s.state == 'open')

                if open_service:
                    print("open service found")
                    continue
                else:

                    part_lines = []
                    for part in record.machine_parts_ids:
                        part_lines.append((0, 0, {
                            'machine_parts_id': part.machine_parts_id.id,
                            'machine_parts_qty': part.machine_parts_qty,
                            'machine_uom_id': part.machine_uom_id
                        }))

                    if today == next_recuring_date:
                        self.create(
                            {
                                'machine_id': record.id,
                                'date': next_recuring_date,
                                'machine_service_parts_ids': part_lines,

                            }
                        )

    """
    machine service state  start
    """

    def machine_service_start(self):

        self.state = 'started'
        self.machine_id.write({'last_service_date': self.date})

    """
    machine service state close
    """

    def machine_service_close(self):

        self.write({'state': 'done'})

        """
        service closing mail
        """

        mail_template = self.env.ref(
            "machine_management.mail_template_servie_completed")

        mail_template.send_mail(self.id, force_send=True)


    """
    machine service state cancel
    """

    def machine_service_cancel(self):
        # self.state = 'cancel'

        self.write({'state': 'cancel'})

    """
    below function is for create invoice for corresponding service & 
    if exist any open(draft) add the  invoice to open invoice default
    service charge is also added. be carful while editing below function!
    
    """

    def machine_service_invoice_creation(self):

        if not self.customer_id:
            raise UserError("Please select a customer")

        service_product = self.env.ref(
            'machine_management.product_service_charge').product_variant_id

        service_charge_line = Command.create({
            'product_id': service_product.id,
            'quantity': 1,
            'price_unit': service_product.list_price,
            'name': service_product.display_name,

        })

        invoice_lines = [service_charge_line]

        for part in self.machine_service_parts_ids:
            invoice_lines.append(Command.create(
                {
                    'product_id': part.machine_parts_id.id,
                    'quantity': part.machine_parts_qty,
                    'price_unit': part.machine_parts_id.list_price,
                    'name': part.machine_parts_id.display_name,
                }
            ))

        if not invoice_lines:
            raise UserError("No parts to invoice.")

        invoice = self.env['account.move'].search([
            ('partner_id', '=', self.customer_id.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'draft')
        ], limit=1)

        if invoice:

            existing_products = invoice.invoice_line_ids.mapped('product_id.id')

            if service_product.id not in existing_products:
                invoice.write({'invoice_line_ids': [
                    Command.create(
                        {
                            'product_id': service_product.id,
                            'quantity': 1,
                            'price_unit': service_product.list_price,
                            'name': service_product.display_name,
                        }
                    )
                ]})

            for part in self.machine_service_parts_ids:
                if part.machine_parts_id:
                    invoice.write({'invoice_line_ids': [
                        Command.create({
                            'product_id': part.machine_parts_id.id,
                            'quantity': part.machine_parts_qty,
                            'price_unit': part.machine_parts_id.list_price,
                            'name': part.machine_parts_id.display_name,

                        })
                    ]})

            # invoice.write({'invoice_line_ids': [(5, 0, 0)] + invoice_lines})
        else:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': invoice_lines,
            })

        self.invoice_id = invoice.id
        self.is_invoice_created = True
        self.is_smart_button_visible = True

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    """
    the below function for paid ribbon in service
    invoice , i used 'payment_sate' from account.move 
    to achieve this.
    """

    @api.depends('invoice_id.payment_state')
    def machine_service_paid(self):
        if self.invoice_id.payment_state == 'paid':
            self.is_ribbon_paid = True
        else:
            self.is_ribbon_paid = False

    def machine_service_invoice_history(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'res_id': self.invoice_id.id,
            'target': 'current',
            'domain': [('id', '=', self.invoice_id.id)],
        }
