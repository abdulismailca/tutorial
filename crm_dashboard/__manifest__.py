{
    'name': "CRM Dash Board",
    'version': '1.0',
    'summary': 'CRM Dash Board OWL',
    'description': 'crm dash board',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase', 'account',
                'crm'],
    'data': [
        'views/crm_team_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
