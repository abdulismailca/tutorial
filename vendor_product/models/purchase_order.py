from odoo import api, fields, models, Command
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    vendor_product_ids = fields.Many2many('product.product','vendor_product_id')
    is_vendor_product = fields.Boolean(string="Is Vendor Product")
    is_lessthan_minimum_amount_po = fields.Boolean(string="All Ready Remove")

    @api.onchange('partner_id')
    def onchange_partner_id(self):


        all_product_filtered = self.env['product.product'].search([('seller_ids.partner_id','=', self.partner_id.id)])

        print("all_product_filtered", all_product_filtered)

        self.update({
            'vendor_product_ids':[(fields.Command.clear())]
        })

        self.update({
            'vendor_product_ids': [(fields.Command.link(a.id)) for a in all_product_filtered]
        })

        his_product_ids = self.vendor_product_ids.mapped('id')
        print("his_product_ids", his_product_ids)


    def button_confirm(self):

        if self.order_line and self.is_lessthan_minimum_amount_po != True :

            print("is_lessthan_minimum_amount_po", self.is_lessthan_minimum_amount_po)



            lessthan_minimum_amount = self.order_line.filtered(lambda s: s.price_unit < 700)

            lessthan_minimum_amount_list =[]
            for l in lessthan_minimum_amount:
                lessthan_minimum_amount_list.append(Command.create({
                    'product_id':l.product_id.id
                }))

            print("lessthan_minimum_amount_list", lessthan_minimum_amount_list)

            if lessthan_minimum_amount:
                lessthan_minimum_amount_po = self.env['purchase.order'].create({
                    'partner_id': self.partner_id.id,
                    'order_line':lessthan_minimum_amount_list,
                    'is_lessthan_minimum_amount_po':True,
                })

                self.update({
                    'order_line': [(fields.Command.unlink(lessthan_minimum_amount.ids))]
                })

        return super(PurchaseOrder, self).button_confirm()





    