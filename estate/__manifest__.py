{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'application': True,
    'auto_install': False,
    'installable': True,
    'website': 'www.cy.com',
    'data': ['security/ir.model.access.csv',
             'views/estate_property_form_view.xml',
             'views/estate_property_search_view.xml',
             'views/estate_property_types_view.xml',
             'views/estate_property_tags_view.xml',
             'views/estate_property_offer_views.xml',
             'views/estate_menu.xml',
             ]
}
