from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    product_brand = fields.Char(string="Brand Name", related='product_id.product_brand', readonly=False)
    product_master_type = fields.Selection(
        [('single_product', 'Single Product'),
         ('brand_product', 'Brand Product')], default="brand_product",
        required=True, related='product_id.product_master_type')



