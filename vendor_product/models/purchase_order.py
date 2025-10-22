from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    vendor_product_ids = fields.Many2many('product.product','vendor_product_id', compute='compute_vendor_product_ids')
    """compute matti onchange akkanam use partner_id"""
    @api.depends()
    def compute_vendor_product_ids(self):
        all_product = self.env['product.product'].search([])

        product_vendor = all_product.mapped('seller_ids')

        all_product_filtered = all_product.filtered(lambda s: self.partner_id in s.seller_ids.partner_id)
        # all_product_filtered = all_product.filtered(lambda s: self.id in s.seller_ids.partner_id)

        print("seller_ids", product_vendor)
        print("all_product_filtered", all_product_filtered)

        self.update({
            'vendor_product_ids': [(fields.Command.link(a.id)) for a in all_product_filtered]
        })
        his_product_ids = self.vendor_product_ids.mapped('id')
        print("his_product_ids", his_product_ids)

# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     @api.onchange('order_id.partner_id')
#     def onchange_vendor_products(self):
#         print("onchange_vendor_products")
#         if self.order_id.partner_id:
#             allowed_products = self.env['product.product'].search([
#                 ('seller_ids.partner_id', '=', self.order_id.partner_id.id)
#             ])
#             return {'domain': {'product_id': [('id', 'in', allowed_products.ids)]}}
#         return {'domain': {'product_id': []}}
    