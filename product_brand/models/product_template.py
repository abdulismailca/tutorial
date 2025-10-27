from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'


    product_brand = fields.Char(string="Brand Name",related='product_variant_id.product_brand')
