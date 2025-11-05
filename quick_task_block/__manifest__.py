{
    'name': "Quick Task Block",
    'version': '1.0',
    'summary': 'some quick task module',
    'description': 'to increase performance',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'product', 'sale_management', 'purchase','website','website_sale'],
    'data': [
        # 'views/product_template_views.xml',
        'views/res_config_settings_view.xml',
        'views/product_card_with_stock.xml',
        # 'views/web_site_cart.xml',
        'views/create_product_website_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
