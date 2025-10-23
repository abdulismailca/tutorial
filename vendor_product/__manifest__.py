{
    'name': "Vendor product",
    'version': '1.0',
    'summary': 'Purchase Orders',
    'description': 'purchase order of vendor',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product','sale_management', 'purchase'],
    'data': [
        'views/purchase_order_views.xml',
        'views/product_product_views.xml'
],



    'installable': True,
    'application': True,
    'auto_install': False,

}
