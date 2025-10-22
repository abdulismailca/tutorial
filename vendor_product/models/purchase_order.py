from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor_order_line_id = fields.Many2one('purchase.order',
                                           string="vendor_order_line_id")

    alternative_product_id = fields.Many2one('product.product',
                                             compute="compute_alternative_product_id")

    @api.onchange('product_id')
    def compute_alternative_product_id(self):
        all_product = self.env['product.product'].search([])

        all_product_filtered = all_product.seller_ids.filtered(
            lambda s: s.partner_id.id == self.partner_id.id)

        print("all_product_filtered", all_product_filtered)

        for venpro in all_product_filtered:
            print("vendor product", venpro.product_tmpl_id.name)



        self.update({
            'alternative_product_id':[(fields.Command.link(a.id)) for a in all_product_filtered]
        })

        # print("alternative_product_id", self.alternative_product_id)
        # 
        # domain = ([('id', 'in', self.alternative_product_id)])
        # 
        # return {'domain': {'product_id': domain}}





class ProductProduct(models.Model):
    _inherit = 'product.template'
    vendor_product_id = fields.Many2one('purchase.order')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_vendor_product = fields.Boolean(string="Is Vendor Product")
    only_vendor_product = fields.Boolean(
        string="Select only this vendor product")
    vendor_order_line_ids = fields.One2many('purchase.order.line',
                                            'vendor_order_line_id',
                                            compute='see_only_vendor_product',
                                            string="Vendor Product",
                                            readonly=False)

    vendor_product_ids = fields.One2many('product.template','vendor_product_id')





    @api.depends('vendor_order_line_ids')
    def see_only_vendor_product(self):
        pass


    @api.onchange('is_vendor_product')
    def vendor_only_product(self):

        if self.is_vendor_product:
            self.update({
                'order_line': [(fields.Command.clear())]
            })
            print("iam from is vendor product")

            all_product = self.env['product.product'].search([])

            all_product_filtered = all_product.seller_ids.filtered(lambda s: s.partner_id.id == self.partner_id.id)

            mapped_product = all_product_filtered.mapped('product_id')
            print("mapped product", mapped_product)

            # all_product_filtered = all_product.purchase_order_line_ids.filtered(lambda s: s.partner_id.id == self.partner_id.id)

            print("model",all_product_filtered)

            for product in all_product_filtered:
                print("Product Name", product.product_tmpl_id.name)


            self.update({
                'vendor_product_ids':[(fields.Command.clear())]
            })

            self.update({
                'vendor_product_ids': [(fields.Command.create({'name':a.product_tmpl_id.name})) for a in all_product_filtered]
            })


            print("product_id", self.product_id)

            domain = ([('id', 'in', [self.vendor_product_ids])])
            return {'domain': {'product_id': domain}}



