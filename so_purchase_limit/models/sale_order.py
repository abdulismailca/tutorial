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
        ]
    )

    approver_1_id = fields.Many2one("res.users", string="Approver 1", help="First approver")
    approver_2_id = fields.Many2one("res.users", string="Approver 2", help="Second approver")
    is_approver_1_approved = fields.Boolean(string="Approver 1 Approved", copy=False)
    is_approver_2_approved = fields.Boolean(string="Approver 2 Approved", copy=False)

    two_step_approve = fields.Integer("Two Step Approval", default=0)



    @api.onchange('approver_1_id')
    def compute_waiting_to_approve(self):
        print("helfddddddddghdfsfgo")
        for rec in self:
            self.approver_1_id = rec.env[
                'ir.config_parameter'].sudo().get_param(
                'so_purchase_limit.approver_1_id')

            self.approver_2_id = rec.env[
                'ir.config_parameter'].sudo().get_param(
                'so_purchase_limit.approver_2_id')

            if rec.amount_total > 25000 and self.env.user.id not in [self.approver_1_id.id, self.approver_2_id.id] :

                print(self.env.user.id)
                print(self.approver_1_id.id)
                print(self.approver_2_id.id)
                rec.state = 'to_approve'

            else:
                rec.state = 'draft'

    def approve_confirm(self):

        print("approve_confirm")
        self.state = "two_to_approve"
        self.two_step_approve = 1

    def two_approve_confirm(self):
        self.two_step_approve = 2
        self.state = 'sale'
        # self.action_confirm()

