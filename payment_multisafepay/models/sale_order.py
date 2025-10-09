from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "sale.order"



    def sale_order_button(self):
        # print(self.order_line)

        sale_order_line_in_odoo = self.env['sale.order'].order_line.search([])
        print("before filter",sale_order_line_in_odoo)

        draft_sate_sale_order = sale_order_line_in_odoo.filtered(lambda s: s.product_uom_qty >= 5 and s.order_id.state == 'draft')

        if draft_sate_sale_order:


            print("after filter",draft_sate_sale_order)
            print("order id",draft_sate_sale_order.mapped('order_id'))
            draft_sate_sale_order.mapped('order_id').action_confirm()


            # sale_order_line_in_odoo.filtered(lambda
            #                                      s: s.product_uom_qty >= 5 and s.order_id.state == 'draft').order_id.action_confirm()


            # sate_draft_so = sale_order_line_in_odoo.filtered(lambda s: s.order_id.state == 'draft')

            # sate_draft_so = sale_order_line_in_odoo.mapped('order_id')
            # sate_draft_only = sate_draft_so.filtered(lambda s: s.state == 'draft')

            # sate_draft_so.action_confirm()

            # print("check", sate_draft_so)

            # print("check", sate_draft_so)



            # for rec in sale_order_line_in_odoo:
            #     print("here here",rec.order_id)
            #     rec.write({'state':'sale'})
            #
            #     # print("ivide nokku ismail", rec.state)
            #
            # print("endho und")

        # if(self.order_line.filtered(lambda s: s.product_uom_qty >= 5)):
        #     raise UserError("Qty is high")

        # for rec in self.order_line:
        #     print( rec.product_uom_qty)
        #     if rec.product_uom_qty >= 5:
        #        raise UserError("Qty is high")
