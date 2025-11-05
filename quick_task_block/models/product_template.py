from odoo import fields, models
from odoo.tools import float_compare


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    # my_delivery_uom_id = fields.Many2one('uom.uom', string="Delivery Uom")
    wh_count = fields.Integer("wh stock", default=9)




class ProductProduct(models.Model):

    _inherit = 'product.product'

    # my_delivery_uom_id = fields.Many2one('uom.uom', string="Delivery Uom")
    wh_count = fields.Integer("wh stock", default=7)


    # def _get_available_quantity(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False, allow_negative=False):
    #     location_id = self.env[
    #         'ir.config_parameter'].sudo().get_param(
    #         'quick_task_block.wh_stock_id') if self.env[
    #         'ir.config_parameter'].sudo().get_param(
    #         'quick_task_block.wh_stock_id') else 0
    #
    #     for rec in self:
    #
    #         product_id = rec.id
    #         quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)
    #         rounding = product_id.uom_id.rounding
    #         if product_id.tracking == 'none':
    #             available_quantity = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
    #             if allow_negative:
    #                 return available_quantity
    #             else:
    #                 return available_quantity if float_compare(available_quantity, 0.0, precision_rounding=rounding) >= 0.0 else 0.0
    #         else:
    #             availaible_quantities = {lot_id: 0.0 for lot_id in list(set(quants.mapped('lot_id'))) + ['untracked']}
    #             for quant in quants:
    #                 if not quant.lot_id and strict and lot_id:
    #                     continue
    #                 if not quant.lot_id:
    #                     availaible_quantities['untracked'] += quant.quantity - quant.reserved_quantity
    #                 else:
    #                     availaible_quantities[quant.lot_id] += quant.quantity - quant.reserved_quantity
    #             if allow_negative:
    #                 self.wh_count = sum(availaible_quantities.values())
    #                 return sum(availaible_quantities.values())
    #             else:
    #                 self.wh_count = sum([available_quantity for available_quantity in availaible_quantities.values()])
    #                 return sum([available_quantity for available_quantity in availaible_quantities.values() if float_compare(available_quantity, 0, precision_rounding=rounding) > 0])



