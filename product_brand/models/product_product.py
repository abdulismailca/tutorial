from email.policy import default

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'


    product_brand = fields.Char(string="Brand Name")
    product_master_type = fields.Selection([('single_product','Single Product'),('brand_product','Brand Product')], default="brand_product", required=True)
    sale_id = fields.Many2one('sale.order')
    product_id = fields.Many2one('product.product')

    his_price_list = fields.Char()


    # self.partner_id.compnay_id.currency_id.symbol

    def on_clik_my_button(self):

        # print(self.product_id.search(['partner_id','=', self.sale_id.patner_id.id]))
        # print(self.sale_id.partner_id.property_product_pricelist)
        # print(self.sale_id.partner_id.property_product_pricelist)

        all_pricelist_rec = self.env['product.pricelist'].search([])
        print("all_pricelist_rec", all_pricelist_rec)
        mapped_item_ids = all_pricelist_rec.item_ids.mapped('product_id')
        print("mapped_item_ids", mapped_item_ids)
        if self.product_id in mapped_item_ids:
            print("helo.....")



        # self.write({'his_price_list':self.sale_id.partner_id.property_product_pricelist.name})




