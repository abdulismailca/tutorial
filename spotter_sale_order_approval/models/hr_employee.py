from email.policy import default

from odoo import fields, models, api


class HrEmployee(models.Model):

    _inherit = 'hr.employee'


    state= fields.Selection([('on_board','On Board'),('off_board','Off Board')], default='on_board')

    @api.onchange('resource_calendar_id')
    def compute_hr_employee_deactivate(self):
        for rec in self:
            if rec.resource_calendar_id:
              rec.state = 'on_board'
              rec.action_unarchive()
            else:
                rec.state = 'off_board'
                rec.action_archive()





