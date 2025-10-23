from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    order_line_vendor_product_ids = fields.Many2many('product.product',
                                          'order_line_vendor_product_id')

    order_line_avg = fields.Float(compute="compute_order_line_avg")


    @api.onchange('product_id')
    def onchange_partner_id(self, parent=None):
        all_product_filtered = self.env['product.product'].search(
            [('seller_ids.partner_id', '=', self.partner_id.id)])

        print("all_product_filtered from orderline", all_product_filtered)

        self.update({
            'order_line_vendor_product_ids': [(fields.Command.clear())]
        })

        self.update({
            'order_line_vendor_product_ids': [(fields.Command.link(a.id)) for a in
                                   all_product_filtered]
        })








