from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    associated_product_ids = fields.One2many("product.template",'associated_product_id')