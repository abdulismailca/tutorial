import json
from odoo.http import content_disposition, request
from odoo.release import description
from odoo.tools import html_escape
from odoo import http
from odoo.http import request

class XLSXReportController(http.Controller):
    """machine management list view"""


    @http.route('/machine/management/list', type='http', auth='public',
                website=True)
    def display_machine_management_list(self, **kwargs):
        print("machine management list")

        machines = request.env['machine.management'].sudo().search([])

        print("machines", machines)
        for t in machines:
            print("Name", t.name)


        return request.render('machine_management.portal_machine_management_list', {
            'machines': machines,
        })
    """machine management form view from home"""

    @http.route(['/my/machine/home/<int:item_id>'], type='http',
                auth="user", website=True)
    def portal_machine_management_portal_detail(self, item_id, **kw):

        print("item id", item_id)

        machine = request.env['machine.management'].browse(item_id).sudo()
        

        print("portal man", machine.name)

        return request.render('machine_management.portal_machine_management_home_form',
                              {'machine': machine, })

    """machine management form view"""

    @http.route(['/my/machine/<int:machine_id>'], type='http',
                auth="user", website=True)
    def portal_machine_management_detail(self, machine_id, **kw):

        machine = request.env['machine.management'].browse(machine_id).sudo()

        print("qwerty", machine.name)

        return request.render('machine_management.portal_machine_management_form',
                              {'machine': machine, })

    """machine transfer from"""

    @http.route(['/my/machine_transfer/<int:transfer_id>'], type='http',
                auth="user", website=True)
    def portal_machine_transfer_detail(self, transfer_id, **kw):

        transfer = request.env['machine.transfer'].browse(transfer_id).sudo()

        print("qwerty", transfer.transfer_date)



        return request.render('machine_management.portal_machine_transfer_page',
                              {'transfer': transfer,})



    """machine transfer list"""

    @http.route('/machine/transfer/list', type='http', auth='public',
                website=True)
    def display_machine_transfer_list(self, **kwargs):
        # print("machine transfer list")

        machines_transfer = request.env['machine.transfer'].sudo().search([])

        # print("machines_transfer", machines_transfer)
        # for t in machines_transfer:
        #
        #     print("Name", t.machine_selection_id)
        #     print("date", t.transfer_date)

        return request.render('machine_management.portal_machine_transfer',{
            'machines_transfer':machines_transfer,
        })




    """create customer in website"""

    @http.route('/create/service/customer', type='http', auth='public', website=True)
    def display_web_create_customer_form(self, **kwargs):


        return request.render('machine_management.website_create_customer_form')


    @http.route('/create/service/customer/action', type='http', auth='public',
                website=True, methods=['POST'])
    def submit_create_customer_request(self, **post):

        print("post data in customer", post)
        name = post.get('name')
        phone = post.get('phone')
        email = post.get('email')
        request.env['res.partner'].sudo().create({
            'name': name,
            'phone': phone,
            'email': email,

        })
        partners = request.env['res.partner'].sudo().search([])

        machines = request.env['machine.management'].sudo().search([])

        return request.render(
            'machine_management.service_request_web_form_template', {
                'partners': partners,
                'machines': machines,
            })





    """service request web site"""



    @http.route('/servicerequest', type='http', auth='public', website=True)
    def display_web_form(self, **kwargs):
        partners = request.env['res.partner'].sudo().search([])

        machines = request.env['machine.management'].sudo().search([])

        return request.render('machine_management.service_request_web_form_template', {
            'partners': partners,
            'machines':machines,
        })


        # return request.render(
        #     'machine_management.service_request_web_form_template')

    @http.route('/servicerequest/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_service_request(self, **post):

        print("post data", post)

        machine_id = post.get('machine_id')
        partner_id = post.get('partner_id')
        date = post.get('date')
        description = post.get('description')



        request.env['machine.service'].sudo().create({
            'machine_id': machine_id,
            'customer_id':partner_id ,
            'date':date,
            'description':description,
        })



        return request.redirect('/contactus-thank-you')


    """below for xlsx report"""
    @http.route('/xlsx_reports', type='http', auth='user',
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name,
                        token='ads'):

        print("inside controller")
        """ Return data to python file passed from the javascript"""
        session_unique_id = request.session.uid
        report_object = request.env[model].with_user(session_unique_id)
        print("Report",report_object)#ith edh model ano 'get_xlsx_report', adhinete object so, a model thane return cheyanam , adh vech function call akkum
        print("model",model)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'), (
                        'Content-Disposition',
                        content_disposition(f"{report_name}.xlsx"))
                             ]
                )
                report_object.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            print("dfghjfgh", e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
            }
            return request.make_response(html_escape(json.dumps(error)))


