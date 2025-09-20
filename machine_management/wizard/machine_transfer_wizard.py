import io
import xlsxwriter

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import json, json_default
import json



class MachineTransferWizard(models.TransientModel):
    _name = "machine.transfer.wizard"
    _description = "Machine Transfer Wizard"

    machine_ids = fields.Many2many("machine.management", string="Machine")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    customer_id = fields.Many2one("res.partner", string="Customer")
    transfer_type = fields.Selection(
        [('install', 'Install'), ('remove', 'Remove')],
        string="Transfer Type"
    )

    def machine_transfer_xl_report(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise UserError("From Date must be less than To Date!")

        query = """
            SELECT mt.id,
                   mt.customer_id,
                   rp.name AS customer_name,
                   mt.transfer_date,
                   mt.transfer_type,
                   mt.machine_selection_id,
                   m.name AS machine_name
            FROM machine_transfer mt
            LEFT JOIN res_partner rp ON rp.id = mt.customer_id
            LEFT JOIN machine_management m ON m.id = mt.machine_selection_id
            WHERE 1=1
        """

        params = {}

        if self.from_date:
            query += " AND mt.transfer_date >= %(from_date)s"
            params['from_date'] = self.from_date

        if self.to_date:
            query += " AND mt.transfer_date <= %(to_date)s"
            params['to_date'] = self.to_date

        if self.customer_id:
            query += " AND mt.customer_id = %(customer_id)s"
            params['customer_id'] = self.customer_id.id

        if self.transfer_type:
            query += " AND mt.transfer_type = %(transfer_type)s"
            params['transfer_type'] = self.transfer_type

        if self.machine_ids:
            query += " AND mt.machine_selection_id IN %(machine_ids)s"
            params['machine_ids'] = tuple(self.machine_ids.ids) if len(
                self.machine_ids) > 1 else (self.machine_ids.id,)

        self.env.cr.execute(query, params)
        transfers = self.env.cr.dictfetchall()

        if not transfers:
            raise UserError("There is No Data to Print!")



        print(json.dumps(transfers,
                                      default=json_default))
        print("button called")
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'report.machine_management.report_machine_transfer',

                'options': json.dumps(transfers,
                                      default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Machine Transfer Excel Report',
            },
            'report_type': 'xlsx',
        }



    def machine_transfer_pdf_report(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise UserError("From Date must be less than To Date!")

        data = {
            'from_date': self.from_date or False,
            'to_date': self.to_date or False,
            'customer_id': self.customer_id.id if self.customer_id else False,
            'transfer_type': self.transfer_type or None,
            'machine_ids': self.machine_ids.ids or [],
        }

        return self.env.ref('machine_management.action_report_machine_transfer').report_action(
            None, data=data
        )
