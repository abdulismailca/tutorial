from odoo import fields, models, api
from odoo.fields import Many2one


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # so_qty_count = fields.Float(string="So Count",
    #                             compute="compute_so_qty_count")
    # po_qty_count = fields.Float(string="Po Count", readonly=True)
    # amount = fields.Float(string="Amount")
    # tax_ids = fields.Many2many('account.tax')
    # calculated_tax = fields.Float(string="Calculated Tax")

    product_tmpl_id = fields.Many2one('product.template')

    sale_order_line_ids = fields.One2many('sale.order.line','res_partner_id')

    qty = fields.Float(string="Qty")
    uom = fields.Many2one('uom.uom', string="uom")
    target_uom = Many2one('uom.uom', string="Target Uom")
    computed_uom = fields.Float("calculated uom")
    uom_category = fields.Many2one('uom.category', related="uom.category_id")

    def calc_uom(self):
        self.computed_uom = self.uom._compute_quantity(
            qty=self.qty,
            to_unit=self.target_uom,
        )


    # def compute_so_qty_count(self):
    #     for rec in self:
    #         all_so = rec.env['sale.order'].search(
    #             [('partner_id', '=', self.id), ('state', '=', 'sale')])
    #
    #         mapped = all_so.order_line.mapped('product_uom_qty')
    #
    #         self.so_qty_count = sum(mapped) if mapped else 0
    #
    #         all_po = rec.env['purchase.order'].search(
    #             [('partner_id', '=', self.id), ('state', '=', 'done')])
    #
    #         mapped = all_po.order_line.mapped('product_qty')
    #
    #         self.po_qty_count = sum(mapped) if mapped else 0
    #
    # def calculate_tax(self):
    #     computed_price = self.tax_ids.compute_all( self.amount, self.currency_id)
    #     self.write({'calculated_tax':computed_price['total_included'] if computed_price else 0})
    #
    #     print("self.sale_order_line_ids", self.sale_order_ids)
    #

    @api.onchange('product_tmpl_id')
    def compute_sale_order_line_ids(self):

        for rec in self:
           if rec.product_tmpl_id:
              print("rec sale ids", rec.sale_order_ids)
              all_so = rec.sale_order_ids.filtered(lambda s: s.order_line.product_template_id == rec.product_tmpl_id)
              print("all_so", all_so)
              all_so_line = all_so.mapped('order_line')
              print("all_so_line", all_so_line)
              rec.update({
                  'sale_order_line_ids': [(fields.Command.clear())]
              })
              rec.update({
                    'sale_order_line_ids':[(fields.Command.link(s.id)) for s in all_so_line]
              })
