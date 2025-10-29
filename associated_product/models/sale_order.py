from odoo import fields, models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    is_associated_products = fields.Boolean(string="Associated Products")
    sale_associated_id = fields.Many2one('purchase.order')


    @api.onchange('is_associated_products')
    def onchange_is_associated_products(self):
       if self.is_associated_products == True:

           partner_associated_produts = self.partner_id.associated_product_ids

           self.update({
               'order_line':[(fields.Command.create({
                   'product_template_id':p.id,
                   'product_uom_qty':1,
                   'partner_id':self.partner_id,
               })) for p in partner_associated_produts]
           })

       if self.is_associated_products == False:
           existing_line = self.order_line.filtered(lambda s: not s.partner_id)
           self.update({
               'order_line': [(fields.Command.clear())]
           })
           self.update({
               'order_line': existing_line
           })
