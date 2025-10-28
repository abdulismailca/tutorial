from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    alternative_sale_order_ids = fields.One2many('sale.order',
                                                 'multiple_invoice_id',
                                                 string="Sale Orders")
    is_existing_invoice_line = fields.Boolean(string="Existing Invoice")



    @api.onchange('alternative_sale_order_ids')
    def onchange_alternative_sale_order_ids(self):

        if self.is_existing_invoice_line == False:
            existing_invoice_line = self.invoice_line_ids



        self.update({
            'invoice_line_ids': [(fields.Command.clear())]
        })


        so_order_line = []

        for so in self.alternative_sale_order_ids:
            for line in so.order_line:
                print("line", line.product_template_id.name)
                so_order_line.append(
                    fields.Command.create({
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                    })

                )

        self.update({
            'invoice_line_ids': so_order_line
        })
        
        # print('existing_invoice_line',existing_invoice_line)
        if self.is_existing_invoice_line == False:
            self.update({
                'invoice_line_ids': [fields.Command.create({
                    'product_id': s.product_id,
                    'quantity': s.quantity,
                    'price_unit': s.price_unit

                }) for s in existing_invoice_line]
            })
            self.is_existing_invoice_line = True



