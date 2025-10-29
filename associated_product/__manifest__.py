{
    'name': "Assciated Product",
    'version': '1.0',
    'summary': 'Asscoiated Products',
    'description': 'Asscoiated Product',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase', 'hr'],
    'data': [

        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/purchase_order_views.xml',
        'views/product_product_views.xml'

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
