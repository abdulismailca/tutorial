from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('to_approve', 'Approve One'),
            ('two_to_approve', 'Approve Two'),
            ('sale', 'Sales Order'),
            ('cancel', 'Cancelled'),
        ], compute="compute_state", store=1
    )

    is_visible_approve_button_one = fields.Boolean(copy=False)
    is_visible_approve_button_two = fields.Boolean(copy=False)

    is_click_approver_b_one = fields.Boolean(copy=False)
    is_click_approver_b_two = fields.Boolean(copy=False)

    is_visible_sale_confirm_b = fields.Boolean(copy=False)




    @api.depends('amount_total')
    def compute_state(self):

        for rec in self:
            if rec.amount_total > 25000:
                rec.is_visible_sale_confirm_b = True
                print("helo ismail C A")
                rec.is_visible_approve_button_one = True
            else:
                print("iam from flase")
                rec.is_visible_sale_confirm_b = False
                rec.is_visible_approve_button_one = False





    def approver_button_one(self):


        print("approve_confirm")
        self.state = "to_approve"
        self.is_click_approver_b_one = True


    def approver_button_two(self):

        self.state = 'draft'
        self.is_click_approver_b_two = True
        self.is_visible_sale_confirm_b = False



    # self.env.user.has_group(
    #     'so_purchase_limit.approver_one') or not self.env.user.has_group(
    #     'so_purchase_limit.approver_two'):
