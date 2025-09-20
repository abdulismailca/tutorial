#
# from odoo import models
# from odoo.exceptions import UserError
# from odoo.tools import unique
#
#
# class MachineTransferXlsx(models.AbstractModel):
#     _name = 'report.machine_management.machine_transfer_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, objs):
#         sheet = workbook.add_worksheet("Machine Transfer Report")
#
#
#
#
#
#         query = """
#             SELECT mt.id,
#                    mt.customer_id,
#                    rp.name AS customer_name,
#                    mt.transfer_date,
#                    mt.transfer_type,
#                    mt.machine_selection_id,
#                    m.name AS machine_name
#             FROM machine_transfer mt
#             LEFT JOIN res_partner rp ON rp.id = mt.customer_id
#             LEFT JOIN machine_management m ON m.id = mt.machine_selection_id
#             WHERE 1=1
#         """
#
#         params = {}
#
#         if data.get('from_date'):
#             query += " AND mt.transfer_date >= %(from_date)s"
#             params['from_date'] = data['from_date']
#
#         if data.get('to_date'):
#             query += " AND mt.transfer_date <= %(to_date)s"
#             params['to_date'] = data['to_date']
#
#         if data.get('customer_id'):
#             query += " AND mt.customer_id = %(customer_id)s"
#             params['customer_id'] = data['customer_id']
#
#         if data.get('transfer_type'):
#             query += " AND mt.transfer_type = %(transfer_type)s"
#             params['transfer_type'] = data['transfer_type']
#
#         if data.get('machine_ids'):
#             query += " AND mt.machine_selection_id IN %(machine_ids)s"
#             params['machine_ids'] = tuple(data['machine_ids'])
#
#         self.env.cr.execute(query, params)
#         transfers = self.env.cr.dictfetchall()
#
#         if not transfers:
#             raise UserError("There is No Data to Print!")
#
#         title_format = workbook.add_format({
#             'bold': True,
#             'align': 'center',
#             'valign': 'vcenter',
#             'font_size': 14,
#             'bg_color': 'red',
#             'border': 1
#         })
#
#         customer_format =workbook.add_format({
#             'bold': True,
#             'align': 'center',
#         })
#
#         transfer_format =workbook.add_format({
#             'bold': True,
#
#         })
#
#
#         header_format = workbook.add_format({
#             # 'bold': True,
#             # 'align': 'center',
#             'valign': 'vcenter',
#             # 'font_color': 'white',
#             # 'bg_color': 'blue',
#             # 'border': 1
#         })
#
#         cell_format = workbook.add_format({
#             'align': 'center',
#             'valign': 'vcenter',
#             'border': 1
#         })
#
#         date_format = workbook.add_format({
#             'num_format': 'yyyy-mm-dd',
#             'align': 'center',
#             'valign': 'vcenter',
#             'border': 1
#         })
#
#         sheet.merge_range('A1:D1', 'MACHINE TRANSFER EXCEL REPORT',
#                           title_format)
#
#
#
#
#
#         all_customer=[]
#         for transfer in transfers:
#             if transfer['customer_name']:
#                 all_customer.append(transfer['customer_name'])
#             unique_customer=list(set(all_customer))
#
#
#         if len(unique_customer)>1:
#             headers = ["Machine", "Customer", "Transfer Type", "Transfer Date"]
#             for col, header in enumerate(headers):
#                 sheet.write(1, col, header, header_format)
#                 sheet.set_column(col, col, 20)
#
#             row = 2
#
#             print("yes iam here")
#             print(len(unique_customer))
#             for transfer in transfers:
#                 if transfer['transfer_type']=='remove':
#                     continue
#                 sheet.write(row, 0, transfer['machine_name'] or "", cell_format)
#                 sheet.write(row, 1, transfer['customer_name'] or "", cell_format)
#                 sheet.write(row, 2, transfer['transfer_type'] or "", cell_format)
#                 if transfer['transfer_date']:
#                     sheet.write_datetime(row, 3, transfer['transfer_date'], date_format)
#                 else:
#                     sheet.write(row, 3, "", cell_format)
#
#                 row += 1
#
#         else:
#             sheet.merge_range('A2:C2','Customer Name:'+unique_customer[0],customer_format)
#
#             headers = ["Machine", "Transfer Type", "Transfer Date"]
#             for col, header in enumerate(headers):
#                 sheet.write(2, col, header, header_format)
#                 sheet.set_column(col, col, 20)
#
#             row = 3
#
#
#             for transfer in transfers:
#
#
#                   if transfer['transfer_type'] == 'remove':
#                       continue
#                   sheet.write(row, 0, transfer['machine_name'] or "", cell_format)
#
#                   sheet.write(row, 1, transfer['transfer_type'] or "",
#                              cell_format)
#                   if transfer['transfer_date']:
#                      sheet.write_datetime(row, 2, transfer['transfer_date'], date_format)
#                   else:
#                       sheet.write(row, 2, "", cell_format)
#
#                   row += 1
#
#
#
#         """
#         remove transfers
#         """
#         remove_count = []
#         for transfer in transfers:
#             if transfer['transfer_type'] == 'remove':
#                 remove_count.append(transfer['transfer_type'])
#
#         if len(remove_count) != 0:
#             print("count", len(remove_count))
#             remove_headers = ["Machine", "Transfer Type", "Transfer Date"]
#
#             sheet.write(row+2,0,'Remove',transfer_format)
#             for col, header in enumerate(remove_headers):
#                 sheet.write(row+3, col, header, header_format)
#                 sheet.set_column(col, col, 20)
#
#
#             for transfer in transfers:
#                 if transfer['transfer_type'] == 'install':
#                     continue
#                 sheet.write(row+4, 0, transfer['machine_name'] or "", cell_format)
#                 sheet.write(row+4, 1, transfer['transfer_type'] or "", cell_format)
#                 if transfer['transfer_date']:
#                     sheet.write_datetime(row+4, 2, transfer['transfer_date'],
#                                          date_format)
#                 else:
#                     sheet.write(row+4, 2, "", cell_format)
#                 row += 1
#
#
#
#
#
