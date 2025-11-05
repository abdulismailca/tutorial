{
    'name': "Approval Block",
    'version': '1.0',
    'summary': 'Approval Block',
    'description': 'Sale Order Approval Block',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase','purchase_stock','stock'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/sale_order_server_action.xml',
        # 'views/sale_order_views.xml',
        # 'views/account_move_views.xml',
        # 'views/account_move_line_views.xml',
        # 'views/res_partner_views.xml'
        # 'views/res_config_settings_views.xml',
        # 'views/ir_cron_data.xml',
        # 'views/email_template.xml',
        # 'views/product_product_views.xml',
        # 'views/res_partner_test_views.xml',
        'views/product_template_views.xml',
        # 'views/sale_order_views_test_three.xml',
        'views/hr_employee_views.xml',
        # 'views/sale_order_server_action.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
