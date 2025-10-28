{
    'name': "Invoice Multiple SO",
    'version': '1.0',
    'summary': 'Purchase Orders',
    'description': 'purchase order of vendor',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product','sale_management', 'purchase', 'account'],
    'data': [
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
    ],



    'installable': True,
    'application': True,
    'auto_install': False,

}
