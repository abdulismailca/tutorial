from odoo import Command,fields, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    is_prime_customer = fields.Boolean(string="Is Prime Customer",  related='partner_id.is_prime_customer')

    def button_confirm(self):

        if self.partner_id.is_prime_customer:
            print("Yes He is prime Customer")
            po_order_line = []
            for line in self.order_line:

                if line.product_master_type == 'brand_product':
                    print("iam from inside line")
                    po_order_line.append(Command.create({
                        'product_id': line.product_id.id,
                        'price_unit':line.price_unit,
                        'product_uom_qty':line.product_uom_qty

                    }))

            so_from_po = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': po_order_line,

            })
            so_from_po.action_confirm()

        return super(PurchaseOrder, self).button_confirm()

