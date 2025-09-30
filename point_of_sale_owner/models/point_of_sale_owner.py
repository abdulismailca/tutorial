from odoo import models, fields

class PosSession(models.Model):
    _inherit = "product.product"



    product_owner = fields.Many2one(related="product_tmpl_id.product_owner" ,string="Product Owner")


    def _load_pos_data_fields(self, config_id):


        fields = super()._load_pos_data_fields(config_id)
        fields.append('product_owner')
        return fields

class ProductRating(models.Model):
    _inherit = "product.template"

    product_owner = fields.Many2one("res.partner", string="Product Owner")