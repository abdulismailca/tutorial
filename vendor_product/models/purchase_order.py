from odoo import api ,fields, models

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    vendor_order_line_id = fields.Many2one('purchase.order', string="vendor_order_line_id")


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    is_vendor_product = fields.Boolean(string="Is Vendor Product")
    only_vendor_product = fields.Boolean(string="Select only this vendor product")
    vendor_order_line_ids = fields.One2many('purchase.order.line', 'vendor_order_line_id' ,compute='see_only_vendor_product', string="Vendor Product", readonly=False)



    def see_only_vendor_product(self):

        vendor_product_only = self.env['purchase.order.line'].search([])


        vendor_product_only_filtered = vendor_product_only.filtered(lambda s: s.partner_id == self.partner_id)

        print("this is", vendor_product_only_filtered)

        for id in vendor_product_only_filtered:

            self.update({
                'vendor_order_line_ids':[(fields.Command.link(id.id))]
            })






    @api.onchange('is_vendor_product')
    def vendor_only_product(self):

        if self.is_vendor_product:
            self.update({
                'order_line': [(fields.Command.clear())]
            })
            print("iam from is vendor product")

            vendor_product_only =self.env['purchase.order.line'].search([])



            vendor_product_only_filtered = vendor_product_only.filtered(
                lambda s: s.partner_id == self.partner_id)


            print("product_only",vendor_product_only_filtered)
            print("self partner_id", self.partner_id.name)
            for id in vendor_product_only_filtered.product_id:
                print("id", id.name)
                for line in self.order_line:
                    self.update({
                        'line.product_id': [(fields.Command.set(id.id))]
                    })















