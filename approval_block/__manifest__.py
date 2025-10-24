{
    'name': "PO Approval Block",
    'version': '1.0',
    'summary': 'Purchase Orders Approval Block',
    'description': 'purchase order approval block',
    'author': 'ismail C A',
    'website': 'www.iza.com',
    'category': 'Management',
    'depends': ['base', 'product','sale_management', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'data/approval_block.xml',
        'views/purchase_order_views.xml',
        'views/approval_block_views.xml',
        'views/approval_block_menu_views.xml',

],



    'installable': True,
    'application': True,
    'auto_install': False,

}
