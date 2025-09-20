

from odoo import models, fields



class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _description = 'employee transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'


    sequence_number = fields.Char(string="Sequence Number", default='New',
                                  readonly=True, copy=False)

    employee_id = fields.Many2one('hr.employee', string='Employee Name', required=True)

    company_id = fields.Many2one('res.company', string='Source Company',
                                 related='employee_id.company_id')

    source_company = fields.Char(string="Source Company", readonly=True)

    transfer_company_id = fields.Many2one('res.company',
                                          string='Destination Company', required=True)

    date = fields.Date(string='Date', required=True)

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_for_approval', 'Waiting for Approval'),
         ('approve', 'Approve'), ('reject', 'Reject')], default='draft')



    def employee_submit_request_button(self):

        for rec in self:
            print("dd",rec.employee_id.transfer_ids)
            print("cc",rec.employee_id.count_of_transfer)

        self.write({'state': 'waiting_for_approval'})



    def employee_request_approve_button(self):


        self.write({'source_company':self.company_id.name})
        self.employee_id.write({'company_id': self.transfer_company_id})
        self.write({'state': 'approve'})



    def employee_request_reject_button(self):
        self.write({'state': 'reject'})

    def create(self, vals):
        if vals.get('sequence_number', 'New') == 'New':
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code(
                'employee.transfer')
        return super(EmployeeTransfer, self).create(vals)

    def employee_rest_to_draft_button(self):
        self.write({'state': 'draft'})
