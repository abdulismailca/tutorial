from odoo import http
from odoo.http import request

class WebsiteProduct(http.Controller):
    @http.route('/newly_machines', auth="public", type='json', website=True)
    def get_newly_machines(self):
        machines = request.env['machine.management'].sudo().search([],order='create_date desc')
        result = []
        for m in machines:
            result.append({
                'id': m.id,
                'name': m.name,
                'date_of_purchase': m.date_of_purchase,
                'purchase_value': m.purchase_value,
                'machine_type':m.machine_type.name if m.machine_type else ' ',
                'serial_number':m.serial_number if m.serial_number else ' ',
                'description':m.description,

            })

        return result