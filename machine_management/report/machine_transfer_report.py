import io

import xlsxwriter

from odoo import api, models
from odoo.exceptions import UserError


class MachineTransferReport(models.AbstractModel):
    _name = 'report.machine_management.report_machine_transfer'
    _description = 'Machine Transfer Report'

    def _get_report_values(self, docids, data=None):




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

        if data.get('from_date'):
            query += " AND mt.transfer_date >= %(from_date)s"
            params['from_date'] = data['from_date']



        if data.get('to_date'):
            query += " AND mt.transfer_date <= %(to_date)s"
            params['to_date'] = data['to_date']

        if data.get('customer_id'):
            query += " AND mt.customer_id = %(customer_id)s"
            params['customer_id'] = data['customer_id']


        if data.get('transfer_type'):
            query += " AND mt.transfer_type = %(transfer_type)s"
            params['transfer_type'] = data['transfer_type']

        if data.get('machine_ids'):
            query += " AND mt.machine_selection_id IN %(machine_ids)s"
            params['machine_ids'] = tuple(data['machine_ids'])


        self.env.cr.execute(query, params)


        columns = [desc[0] for desc in self.env.cr.description]


        rows = self.env.cr.fetchall()


        docs = [dict(zip(columns, row)) for row in rows]


        if len(rows)==0:

            raise UserError("There is No Data to Print!")




        # ttt = self.env.cr.dictfetchall()
        # print("rrrrwwww")


        return {
            'doc_model': 'machine.transfer',
            'docs': docs,
        }

    def get_xlsx_report(self, data, response):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Machine Transfer")

        header_format = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 14})
        label_format = workbook.add_format(
            {'font_size': 11, 'bold': True, 'align': 'center', 'border': 1,
             'bg_color': 'blue'})
        text_format = workbook.add_format({'font_size': 11, 'border': 1})
        center_format = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'border': 1})

        sheet.merge_range('A1:D1', 'Machine Transfer Excel Report',
                          header_format)

        row = 3

        all_customer = [d['customer_id'] for d in data if d.get('customer_id')]
        unique_customers = list(set(all_customer))

        installs = [t for t in data if t['transfer_type'] == 'install']
        removes = [t for t in data if t['transfer_type'] == 'remove']

        if installs:
            if len(unique_customers) > 1:
                sheet.write(row, 0, 'Customer Name', label_format)
                sheet.write(row, 1, 'Transfer Date', label_format)
                sheet.write(row, 2, 'Transfer Type', label_format)
                sheet.write(row, 3, 'Machine Name', label_format)
                row += 1

                for transfer in installs:
                    sheet.write(row, 0, transfer.get('customer_name') or '',
                                text_format)
                    sheet.write(row, 1,
                                str(transfer.get('transfer_date') or ''),
                                center_format)
                    sheet.write(row, 2, transfer.get(
                        'transfer_type').capitalize() or '', text_format)
                    sheet.write(row, 3, transfer.get('machine_name') or '',
                                text_format)
                    row += 1

                for col in range(4):
                    sheet.set_column(col, col, 20)

            else:
                if data[0].get('customer_name'):
                    sheet.merge_range('A2:D2',
                                      'Customer: ' + data[0]['customer_name'])

                sheet.write(row, 0, 'Machine Name', label_format)
                sheet.write(row, 1, 'Transfer Type', label_format)
                sheet.write(row, 2, 'Transfer Date', label_format)
                row += 1

                for transfer in installs:
                    sheet.write(row, 0, transfer.get('machine_name') or '',
                                center_format)
                    sheet.write(row, 1, transfer.get(
                        'transfer_type').capitalize() or '', text_format)
                    sheet.write(row, 2,
                                str(transfer.get('transfer_date') or ''),
                                text_format)
                    row += 1

                for col in range(4):
                    sheet.set_column(col, col, 20)

        if removes:

            if installs:
                row += 2

            sheet.write(row, 0, 'Machine Name', label_format)
            sheet.write(row, 1, 'Transfer Type', label_format)
            sheet.write(row, 2, 'Transfer Date', label_format)
            row += 1

            for transfer in removes:
                sheet.write(row, 0, transfer.get('machine_name') or '',
                            center_format)
                sheet.write(row, 1,
                            transfer.get('transfer_type').capitalize() or '',
                            text_format)
                sheet.write(row, 2, str(transfer.get('transfer_date') or ''),
                            text_format)
                row += 1

            for col in range(3):
                sheet.set_column(col, col, 20)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

