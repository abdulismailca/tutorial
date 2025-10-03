{
    'name': "Pos Purchase Limit",
    'version': '1.0',
    'depends': ['base', 'point_of_sale'],
    'application': True,
    'auto_install': False,
    'installable': True,
    'website': 'www.ca.com',
    'data': [
        'views/pos_purchase_limit_views.xml',
        'views/pos_settings_purchase_limit.xml',

    ],

    'assets': {
        'point_of_sale._assets_pos': [

            'pos_purchase_limit/static/src/js/pos_purchase_limt.js',
            'pos_purchase_limit/static/src/js/popup_component.js',
            'pos_purchase_limit/static/src/xml/popup.xml',

        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,

}
