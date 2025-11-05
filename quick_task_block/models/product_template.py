from odoo import fields, models, api
from odoo.tools import float_compare

class ProductTemplate(models.Model):

    _inherit = 'product.template'


    # my_delivery_uom_id = fields.Many2one('uom.uom', string="Delivery Uom")
    wh_count = fields.Integer("wh stock", default=9,compute="_compute_specific_location_qty")


    def _compute_specific_location_qty(self):
        # Get the location ID from system parameters
        print("helo ismial")
        location_id = int(
            self.env['ir.config_parameter'].sudo().get_param('quick_task_block.wh_stock_id', default=0))
        print("location_id", location_id)
        for product in self:
            if not location_id:
                product.specific_location_qty = 0.0
                continue


            quants = self.env['stock.quant'].sudo().search([
                ('product_id', 'in', product.product_variant_ids.ids),
                ('location_id', '=', location_id)
            ])

            product.wh_count = sum(quants.mapped('quantity'))








