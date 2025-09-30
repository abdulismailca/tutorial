{
    'name': "Point of Sale Owner",
    'version': '1.0',
    'depends': ['base', 'point_of_sale'],
    'application': True,
    'auto_install': False,
    'installable': True,
    'website': 'www.ca.com',
    'data': [
        'views/point_of_sale_product_owner_views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'point_of_sale_owner/static/src/js/product_owner.js',

           'point_of_sale_owner/static/src/xml/product_owner_receipt.xml',
           'point_of_sale_owner/static/src/xml/product_owner_screen.xml',
            # 'point_of_sale_rating/static/src/xml/quality_recipt.xml',
            # 'point_of_sale_rating/static/src/xml/quality_table_recipt.xml',

        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,

}
