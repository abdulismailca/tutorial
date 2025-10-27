{
    'name': "Product Brand",
    'version': '1.0',
    'summary': 'Product Brand',
    'description': 'Brand of the Product',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product','sale_management', 'purchase'],
    'data': [
        'views/product_product_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/hr_employee_views.xml',
        # 'views/product_template_views.xml',
        # 'views/sale_order_line_views.xml',
],



    'installable': True,
    'application': True,
    'auto_install': False,

}
