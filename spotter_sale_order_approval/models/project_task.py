from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError, ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.onchange('timesheet_ids', 'user_ids')
    def onchange_timesheet_ids_user_ids(self):
        if self.total_hours_spent > self.allocated_hours:
            raise UserError('Time Exceed')

        if len(self.user_ids) > 1:
            raise UserError('Please Select One User Only')

        for rec in self.timesheet_ids:
            all_data = self.timesheet_ids.filtered(lambda d: d.date == rec.date)

            mapped_all_data = all_data.mapped('unit_amount')

            if sum(mapped_all_data) > rec.employee_id.resource_calendar_id.hours_per_day:
                raise UserError('Please Assign His time Only')
