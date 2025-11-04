from odoo import fields, models




class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values):
        my_delivery_uom_id = product_id.my_delivery_uom_id
        converted_quantity = product_uom._compute_quantity(product_qty,
                                                           my_delivery_uom_id)

        print("my_delivery_uom_id",my_delivery_uom_id.name)
        print("converted_quantity",converted_quantity)

        product_uom = my_delivery_uom_id
        product_qty = converted_quantity

        return super()._get_stock_move_values(product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values)