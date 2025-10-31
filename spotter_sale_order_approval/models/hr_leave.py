from datetime import timedelta, date

from odoo import fields, models
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # def action_approve(self):
    #     all_leave_data = self.search([('user_id', '=', self.env.user.id),
    #                                   ('holiday_status_id', '=',
    #                                    self.holiday_status_id.id),
    #                                   ('state', '=', 'validate')],
    #                                  order="create_date desc", limit="1")
    #     if all_leave_data:
    #         date_diffrence = self.request_date_from - all_leave_data.request_date_to
    #         if date_diffrence >= timedelta(days=5):
    #             raise ValidationError(
    #                 "You Cant take this leave, you took this recently")
    #     return super(HrLeave, self).action_approve()


    # def send_leave_details_mail(self):
    def action_approve(self):
        all_leave_request = self.search([('request_date_to','<',date.today())])


        if all_leave_request:

            for rec in all_leave_request:

                mail_template = rec.env.ref("machine_management.mail_template_hr_leave_details")

                mail_template.send_mail(rec.id, force_send=True)


        raise ValidationError("kkk")

        return super(HrLeave, self).action_approve()

