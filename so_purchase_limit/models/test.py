from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'




    state = fields.Selection(
        selection_add=[
            ('draft','Quotation'),
            ('sent','Quotation Sent'),
            ('to_approve', 'To Approve'),
            ('sale','Sales Order'),
            ('cancel','Cancelled'),
        ], compute="compute_waiting_to_approve", store="1"
    )

    approver_1_id = fields.Many2one("res.users", string="Approver 1", help="First approver")
    approver_2_id = fields.Many2one("res.users", string="Approver 2", help="Second approver")


    is_visible_approve_button = fields.Boolean(string="Visible Approve Button")

    @api.depends('amount_total')
    def compute_waiting_to_approve(self):
        print("helo")
        for rec in self:
            # base.group_system
            if rec.amount_total > 100 and not self.env.user.has_group('base.group_sale_manager'):
               rec.state = 'to_approve'

            else :
                rec.state = 'draft'


    @api.depends('state')
    def compute_state(self):

        # or self.env.user.has_group('sales_team.group_sale_manager')
        if self.state == 'to_approve' and  self.env.user.has_group('base.group_sale_manager'):

           self.is_visible_approve_button = True

    def approve_waiting(self):

        self.action_confirm()



sale_management.group_saleman_all_docs
sale_management.group_saleman_own_docs
