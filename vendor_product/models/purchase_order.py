from odoo import api ,fields, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    is_vendor_product = fields.Boolean(string="Is Vendor Product")


    @api.onchange('is_vendor_product')
    def vendor_only_product(self):


        if self.is_vendor_product:
            print("self partner id",self.partner_id)
            partner_list = []
            for line in self.order_line:
                partner_list.append(line.product_id.purchase_order_line_ids.partner_id)

            print("purchase order line partner id",partner_list)

            if not self.partner_id in partner_list:
                self.update({
                    'order_line': [(fields.Command.clear())]
                })





