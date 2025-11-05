import base64
import json
from odoo.http import content_disposition, request
from odoo.release import description
from odoo.tools import html_escape
from odoo import http
from odoo.http import request
from odoo.tools.image import binary_to_image


class XLSXReportController(http.Controller):
    

    @http.route('/servicerequest', type='http', auth='public', website=True)
    def display_web_form(self, **kwargs):


        # machines = request.env['product.product'].sudo().search([])
        print("machines")

        return request.render('quick_task_block.create_product_form')


        # return request.render(
        #     'machine_management.service_request_web_form_template')

    @http.route('/create/product', type='http', auth='public', website=True, methods=['POST'])
    def submit_service_request(self, **post):

        print("post data", post)

        # product_id = post.get('machine_id')
        # quantity = post.get('description')
        # order = request.website.sale_get_order()
        #
        # print("product_id", product_id)
        #
        # order._cart_update(
        #     product_id=int(product_id),
        #     add_qty=quantity,
        #     set_qty=0
        # )


        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': 'Greetings!',
        #         # 'message': f'Hello {self.name}, your action was successful.',
        #         'type': 'success',
        #         'sticky': False
        #     }
        # }

        name = post.get('name')
        my_image = post.get('my_image')
        my_convert_img = base64.b64encode(my_image.read().decode('utf-8'))
        print("my_convert_img", my_convert_img)

        list_price =post.get('price')
        request.env['product.product'].sudo().create({
            'name':name,
            'website_published':True,
            'is_published':True,
            'list_price':list_price,
            'image_1920':my_convert_img,

        })

        # return request.redirect("/shop/cart")

        order = request.website.sale_get_order()
        print("order", order)




        # request.env['machine.service'].sudo().create({
        #     'machine_id': machine_id,
        #     'customer_id':partner_id ,
        #     'date':date,
        #     'description':description,
        # })



        return request.redirect('/contactus-thank-you')
    #
    #
