from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

       for line in self.order_line:



           sale_price = line.price_unit
           cost_price = line.product_template_id.standard_price
           cost_price_percentage = ((cost_price/100)*15) + cost_price

           print("Cost + 15%",cost_price_percentage)

           print("Sales Price",sale_price)
           print("Cost Price",cost_price)
           if sale_price < cost_price_percentage:
               raise UserError("Sale price must be greater than cost price")

       return super(SaleOrder, self).action_confirm()

