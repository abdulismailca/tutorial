from email.policy import default

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'


    product_brand = fields.Char(string="Brand Name")
    product_master_type = fields.Selection([('single_product','Single Product'),('brand_product','Brand Product')], default="brand_product", required=True)


    partner_id = fields.Many2one('res.partner', string="Partner")
    product_id = fields.Many2one('product.product')
    his_rate = fields.Float(string="His Rate")

    """"to fetch currency of res_partner"""
    # self.partner_id.compnay_id.currency_id.symbol

    def on_clik_my_button(self):
        print(self.partner_id.property_product_pricelist)
        if self.partner_id.property_product_pricelist:
           price_list =  self.partner_id.property_product_pricelist
           price = price_list._get_product_price(self.product_id,1,self.partner_id)
           print("price",price)
           self.write({'his_rate':price})




