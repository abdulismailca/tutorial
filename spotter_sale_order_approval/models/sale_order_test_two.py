from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.model
    def so_unit_to_dozen(self):

        all_so = self.search([('state','=','draft')])

        all_so_order_line = all_so.mapped('order_line')

        print("all_so_order_line", all_so_order_line)
        donzen_id = self.order_line.product_uom.search([('name','=','Dozens')])
        print("donzen_id", donzen_id)
        for rec in all_so_order_line:

            rec.product_uom = donzen_id.id

