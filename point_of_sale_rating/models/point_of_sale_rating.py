from odoo import models, fields

class PosSession(models.Model):
    _inherit = "product.product"


    # quality_product_id = fields.Many2one('product.template', string="Product")
    quality_rating = fields.Selection(related="product_tmpl_id.quality_rating" ,string="Quality Rating")


    def _load_pos_data_fields(self, config_id):
        # for ff in self.product_tmpl_id:
        #     print("helo..",ff.id)

        fields = super()._load_pos_data_fields(config_id)
        fields.append('quality_rating')
        return fields

class ProductRating(models.Model):
    _inherit = "product.template"
    # for_quality_relation_ids = fields.One2many("product.product","quality_product_id")
    quality_rating = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        string="Quality Rating",
        default='3'
    )