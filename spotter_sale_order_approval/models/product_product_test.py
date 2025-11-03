
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_total_value = fields.Float("Product Total Value", compute="compute_product_total_value", store=1)





    def compute_product_total_value(self):

        for rec in self:
            print("helo", rec.id)
            rec.product_total_value = rec.total_value
