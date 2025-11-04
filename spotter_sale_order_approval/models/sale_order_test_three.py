from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

    _inherit ='sale.order'

    my_product_tmpl_id = fields.Many2one('product.template')

    my_category_id = fields.Many2one('uom.category')

    is_active_my_category_id = fields.Boolean()




    def action_confirm(self):

        # move_line_ids
        # product_uom
        # sale_id
        all_move = self.picking_ids.search([('sale_id','=',self.id)])
        all_move_move_line = all_move.mapped('move_line_ids')
        print(all_move_move_line)




        for rec in all_move_move_line:

            new_uom_value =rec.product_uom._compute_quantity(
                qty=rec.quantity,
                to_unit=rec.product_id.my_delivery_uom_id,
            )
            rec.product_uom_qty=new_uom_value



        raise ValidationError("kkkk")
        return super(SaleOrder, self).action_confirm()