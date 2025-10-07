{
    'name': "Purchase Order Tab",
    'version': '1.0',
    'summary': 'Purchase Orders',
    'description': 'purchase order on product',
    'author': 'ismail C A',
    'website': 'www.isa.com',
    'category': 'Management',
    'depends': ['base', 'product','sale_management', 'purchase'],
    'data': [
        'views/purchase_tab_views.xml',
        'views/purchase_order_smart_button_views.xml',
],



    'installable': True,

    'application': True,
    'auto_install': False,

}
