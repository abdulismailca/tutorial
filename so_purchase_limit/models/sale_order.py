from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('to_approve', 'To Approve'),
            ('two_to_approve', 'Approved'),
            ('sale', 'Sales Order'),
            ('cancel', 'Cancelled'),
        ], compute="compute_state", store=1
    )

    approver_1_id = fields.Many2one("res.users", string="Approver 1",
                                    help="First approver")
    approver_2_id = fields.Many2one("res.users", string="Approver 2",
                                    help="Second approver")

    two_step_approve = fields.Integer("Two Step Approval", default=0)

    @api.depends('amount_total')
    def compute_state(self):

        for rec in self:
            if rec.amount_total > 25000 and rec.state != 'two_to_approve':
                rec.state = 'to_approve'
                self.two_step_approve = 1

            else:
                rec.state = 'draft'

    def approve_confirm(self):


        print("approve_confirm")
        self.state = "two_to_approve"
        self.two_step_approve = 1

    def two_approve_confirm(self):


        self.two_step_approve = 2
        self.state = 'draft'
