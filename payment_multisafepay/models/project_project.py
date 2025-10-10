
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class ProjectProject(models.Model):
    _inherit = "project.project"

    progress = fields.Integer(string="Progress", compute="compute_progress")


    def compute_progress(self):
        print("helo")

        all_task = self.task_ids

        status_complete_task = all_task.stage_id.name.search([('state','=','done')])




