from datetime import date, datetime

from odoo import fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):

    _inherit = "sale.order"

    project_id = fields.Many2one("project.project", string="Project")
    his_own_project = fields.Many2many("project.project", compute="compute_his_project")

    def compute_his_project(self):

        for cus in self.project_id:
            print(cus.partner_id.name)
        his_project = self.project_id.filtered(lambda s: s.partner_id == self.partner_id)


        print("project_id",his_project)

        print(his_project)

        self.update({
            'his_own_project': [(fields.Command.link(a.id)) for a in his_project]
        })




