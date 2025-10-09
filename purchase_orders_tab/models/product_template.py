from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.product"
    purchase_orders_ids = fields.Many2many('purchase.order', string="Purchase Order", compute="own_product_purchase")
    purchase_orders_count = fields.Integer(string="Count Of PO")


    def own_product_purchase(self):
         print("helo")
         # len_of = len(self.purchase_orders_ids)
         # print(len_of)
         # print("iipo endelum undo",self.po_ids)

         for rec in self:
             purchase_rders = rec.purchase_orders_ids.search([('product_id', 'in', [self.id])])

         count_of_purchase_order = len(purchase_rders)
         print("count undo", count_of_purchase_order)

         # self.purchase_orders_count = count_of_purchase_order

         self.write({'purchase_orders_count':len(purchase_rders)})




         self.update({
                       'purchase_orders_ids': [(fields.Command.link(a.id)) for a in purchase_rders]
                   })

    def count_of_po(self):
        pass

        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Purchase Order',
        #     'res_model': 'purchase.order',
        #     'view_mode': 'list,form',
        #     'domain': [('product_id', 'in', [self.id])],
        #
        # }

         #    print("wert",rec.purchase_orders_ids.product_id)
         #    purchase_rders = rec.purchase_orders_ids.search(
         #        [('product_id','=',self.id)]
         #    )
         # print("hjm", purchase_rders)

         #
         # orders = self.purchase_orders_ids.search([
         #
         #     ('product_id','=', self.id)
         # ])

         # print("orders",orders)





    # def action_view_po(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("purchase.action_purchase_history")
    #     action['domain'] = [
    #         ('state', 'in', ['purchase', 'done']),
    #         ('product_id', 'in', self.with_context(active_test=False).product_variant_ids.ids),
    #     ]
    #     action['display_name'] = _("Purchase History for %s", self.display_name)
    #     return action






