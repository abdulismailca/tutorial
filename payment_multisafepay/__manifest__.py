# -*- coding: utf-8 -*-
{
    'name': "Payment Multisafepay",
    'version': "18.0.1.0.0",
    'summary': """Multisafepay Payment Integration""",
    'description': "Multisafepay Payment",
    'author': "Anjali",
    'category': "Payment",
    'sequence': 1,
    'depends':['base','website','payment'],
    'data': [
        "data/account_payment_method.xml",
        "data/payment_method_data.xml",
        "data/payment_provider_data.xml",
        "views/payment_templates.xml",
        "views/payment_provider_views.xml",
        "views/payment_transaction_views.xml",
    ],
    'installable': True
}



