from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    sale_associated_ids = fields.Many2many('sale.order','sale_associated_id')


    def button_confirm(self):


        all_po_with_same_so = self.search([])


        filtered_all_po_with_same_so = all_po_with_same_so.filtered(lambda s: s.sale_associated_ids.ids == self.sale_associated_ids.ids)-self



        filtered_all_po_with_same_so.button_cancel()
        # raise ValidationError("kkkkk")
        return super(PurchaseOrder, self).button_confirm()