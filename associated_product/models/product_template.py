from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'


    associated_product_id = fields.Many2one('res.partner')