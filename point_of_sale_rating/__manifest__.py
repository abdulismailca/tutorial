{
    'name': "Point of Sale Rating",
    'version': '1.0',
    'depends': ['base','point_of_sale'],
    'application': True,
    'auto_install': False,
    'installable': True,
    'website': 'www.ca.com',
    'data': [
       'views/point_of_sale_rating_views.xml',

    ],

'assets': {

'web.assets_frontend': [
            'point_of_sale_rating/static/src/js/rating.js'
        ],
    'point_of_sale._assets_pos': [
        'point_of_sale_rating/static/src/xml/pos_screen.xml',
   ]
},

    'installable': True,
    'application': True,
    'auto_install': False,

}
