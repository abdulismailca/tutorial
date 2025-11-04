from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'


    def action_confirm(self):
        if self.opportunity_id:
            self.opportunity_id.stage_id = self.team_id.stage_id if self.team_id.stage_id else 0
        return super(SaleOrder, self).action_confirm()