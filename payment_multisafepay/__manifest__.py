{
    'name': 'Multisafepay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,


    'website': 'www.iza.com',
    'depends': ['base','sale_management'],
    'data': [
        # 'data/payment_provider_data.xml',
        # 'views/payment_multisafepay_templates.xml',
        # 'views/payment_provider_views.xml',
        'views/sale_order_views.xml'


    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',

}
