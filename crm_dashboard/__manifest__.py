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
        'views/crm_dashboard_menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            # 'crm_dashboard/static/src/js/dashboard.js',

            'crm_dashboard/static/src/js/lib/Chart.bundle.js',
            'crm_dashboard/static/src/xml/dashboard.xml',
            'crm_dashboard/static/src/js/lib/Chart.bundle.js',
            'crm_dashboard/static/src/js/tile.js',
            # 'crm_dashboard/static/src/js/filter.js',


        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,

}
