

from odoo import api, fields, models

class PointOfSaleRating(models.Model):

    _inherit = "product.template"

    quality_rating = fields.Selection([('one','1'),('two','2'),('three','3'),('four','4'),('five','5')],   string="Quality Rating" ,default="one")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['quality_rating']
        return data


# from odoo import , fields, models
# class CustomModel(models.Model):
#    """Inherit the custom model to add a new field and add the field to the pos"""
#    _inherit = 'custom.model'
#    _description = 'custom model'
#    age = fields.Integer(string="Age")
#    @api.model
#    def _load_pos_data_fields(self, config_id):
#        data = super()._load_pos_data_fields(config_id)
#        data += ['age']
#        return data