from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = "product.product"



    product_owner_id = fields.Many2one(related="product_tmpl_id.product_owner_id" ,string="Product Owner")


    product_owner_name = fields.Char(related="product_owner_id.name", string="Product Owner Name")


    def _load_pos_data_fields(self, config_id):


        fields = super()._load_pos_data_fields(config_id)
        fields.append('product_owner_name')
        return fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_owner_id = fields.Many2one("res.partner", string="Product Owner")