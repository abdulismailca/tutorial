{
    'name': "Machine Management",
    'version': '1.0',
    'summary': 'From machine creation to transfer',
    'description': 'Easy mangment of machines',
    'author': 'ismail C A',
    'website': 'www.isa.com',
    'category': 'Management',
    'depends': ['base', 'mail', 'product', 'account', 'website','website_sale'],
    'data': [
        'security/machine_user_group.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/ir_cron_data.xml',
        'data/machine_types_default_data.xml',
        'data/machine_sequence_data.xml',
        'data/machine_service_product_data.xml',

        'report/ir_actions_report.xml',
        'report/machine_transfer_report.xml',

        'wizard/machine_transfer_report_wizard_view.xml',
        'views/machine_types_views.xml',
        'views/machine_tags_views.xml',
        'views/machine_res_partner_views.xml',
        'views/machine_parts_views.xml',
        'views/machine_management_views.xml',
        'views/machine_transfer_views.xml',
        'views/machine_service_views.xml',
        'views/machine_menu_views.xml',
        'views/machine_service_request_menu_views.xml',
        'views/machine_snippet_view.xml',
        'views/clear_cart_button_views.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'machine_management/static/src/js/action_manager.js',

        ],
        'web.assets_frontend': [
            'machine_management/static/src/js/machine_dynamic_content.js',
            'machine_management/static/src/xml/machine_dynamic_snippet.xml',
        ],
    },

    'installable': True,

    'application': True,
    'auto_install': False,

}
