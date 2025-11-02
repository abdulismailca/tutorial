{
    'name': "SO Approval Block",
    'version': '1.0',
    'summary': 'Sale Order Approval Block',
    'description': 'Sale Order Approval Block',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase', 'account','crm'],
    'data': [

        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
