# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: Multisafepay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A indian, kerala payment provider covering several Asian countries.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'author': 'C A LLC',
    'website': 'https://www.iza.com',
    'depends': ['payment'],
    'data': [
        'views/payment_mollie_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',

}
