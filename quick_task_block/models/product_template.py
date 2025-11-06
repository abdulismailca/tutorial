from odoo import fields, models, api
from odoo.tools import float_compare


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    wh_count = fields.Integer(string="wh stock", default=7,
                              compute="_compute_specific_location_qty")

    def _compute_specific_location_qty(self):
        location_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'quick_task_block.wh_stock_id', default=0))
        for product in self:
            if not location_id:
                product.wh_count = 0
                continue
            obj_location = self.env['stock.location'].browse(location_id)
            quants = product.env['stock.quant']._get_available_quantity(
                product_id=product.product_variant_id,
                location_id=obj_location)
            product.wh_count = quants
