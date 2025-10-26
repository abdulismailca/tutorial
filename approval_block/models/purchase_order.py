from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    approval_block_id = fields.Many2one('approval.block',
                                        compute="compute_approval_block_id")

    @api.depends('amount_total')
    def compute_approval_block_id(self):
        if self.amount_total <= 5000:
            five_rc = self.approval_block_id.search(
                [('limit_amount', '=', 5000)])
            print("five_rc", five_rc)
            self.write({'approval_block_id': five_rc})
            # self.approval_block_id = five_rc

        else:
            ten_rc = self.approval_block_id.search(
                [('limit_amount', '=', 10000)])
            # self.approval_block_id = ten_rc
            self.write({'approval_block_id': ten_rc})




















