from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    avg_of_p = fields.Float(compute="compute_avg_of_p")

    @api.depends()
    def compute_avg_of_p(self):
        this_product_purchase_order = self.env['purchase.order'].search([('order_line.product_id','=',self.id)])

        print("this_product_purchase_order", this_product_purchase_order)


        product_price_unit = sum(this_product_purchase_order.mapped('order_line.price_unit'))
        print("product_price_unit", product_price_unit)

        mapped_price_sub_total = product_price_unit/len(this_product_purchase_order)

        print("mapped_price_sub_total", mapped_price_sub_total)

        print("self", self.id)
        self.write({'avg_of_p':mapped_price_sub_total if mapped_price_sub_total else 0})