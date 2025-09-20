from email.policy import default

from odoo import models, fields, api


class HrEmployee(models.Model):


    _inherit = 'hr.employee'



    transfer_ids = fields.One2many('employee.transfer','employee_id',store=True)

    count_of_transfer = fields.Integer(compute="compute_count_of_transfer",store=True)

    @api.depends('transfer_ids')
    def compute_count_of_transfer(self):
        count = len(self.transfer_ids)
        self.write({'count_of_transfer':count})














