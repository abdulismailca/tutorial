{
    'name': "SO Approval Block",
    'version': '1.0',
    'summary': 'Sale Order Approval Block',
    'description': 'Sale Order Approval Block',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase', 'hr'],
    'data': [
        # 'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
