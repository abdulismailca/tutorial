from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    approval_block_id = fields.Many2one('approval.block',
                                        compute="compute_approval_block_id", store=True)

    @api.depends('amount_total')
    def compute_approval_block_id(self):
        print("hhhhhhhh")
        full_block = self.approval_block_id.search([('limit_amount','<=',self.amount_total)], order='limit_amount desc',limit=1)
        print("hai iam from", full_block.limit_amount)
        full_data = self.approval_block_id.search([])

        filtered_data = full_data.filtered(lambda s: s.limit_amount <= self.amount_total)
        print('Sorted',filtered_data.sorted(lambda s: s.limit_amount,reverse=True))
        s_data = filtered_data.sorted(lambda s: s.limit_amount,reverse=True)

        self.write({'approval_block_id':s_data[0] if s_data[0] else '' })





















