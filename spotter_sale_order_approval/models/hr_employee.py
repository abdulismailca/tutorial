from email.policy import default

from odoo import fields, models, api


class HrEmployee(models.Model):

    _inherit = 'hr.employee'


    state= fields.Selection([('on_board','On Board'),('off_board','Off Board')], default='on_board', compute="compute_hr_employee_deactivate")


    def compute_hr_employee_deactivate(self):

        for rec in self:
            if rec.resource_calendar_id:
              rec.state = 'off_board'
              print("helo")
              rec.action_unarchive()
              # rec.active= True
              break
            else:
                print('hai')
                rec.state = 'on_board'
                rec.action_archive()
                # rec.active = True
                break




