from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    my_delivery_uom_id = fields.Many2one('uom.uom', string="Delivery uom")
    my_uom_category_id = fields.Many2one('uom.category')

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    my_delivery_uom_id = fields.Many2one('uom.uom', string="Delivery uom")

