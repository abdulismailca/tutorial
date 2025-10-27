from odoo import fields, models


class SalseOrderLine(models.Model):
    _inherit = 'sale.order.line'


    product_brand = fields.Char(string="Brand Name", related='product_template_id.product_brand', readonly=False)