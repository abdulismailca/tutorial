from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'
    state = fields.Selection([('vendor','Vendor'),('customer','Customer'),('both','both')],compute="compute_state")

    def compute_state(self):
        if self.customer_rank > 0 and self.supplier_rank > 0:
            self.state = 'both'
        elif self.supplier_rank > 0:
            self.state= 'vendor'
        else :
            self.state = 'customer'







