

from odoo import api, fields, models
class PointOfSaleRating(models.Model):

   _inherit = "product.template"

   quality_rating = fields.Selection(
       [('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'),
        ('five', '5')], string="Quality Rating", default="one")

   @api.model
   def _load_pos_data_fields(self, config_id):
       print("iam here")
       data = super()._load_pos_data_fields(config_id)
       print("what is this ", data)
       data += ['quality_rating']

       print("now what is this ", data)
       return data

