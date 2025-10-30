from odoo import fields, models



class MyInvoiceLine(models.Model):

    _name ='my.invoice.line'
    _description = "my invoice line"

    my_invoice_id = fields.Many2one('account.move')
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    price_unit = fields.Float()
    price_subtotal = fields.Float()

    move_id = fields.Many2one('account.move.line')


    def add_invoice_line(self):
        invoice = self.env['account.move.line'].create({

            'product_id': self.product_id.id,
            'quantity': self.quantity,
            'price_unit': self.price_unit,
            'price_subtotal': self.price_subtotal,
            'move_id': self.my_invoice_id.id
        })
        self.unlink()




