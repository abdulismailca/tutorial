{
    'name': "Employee Transfer",
    'version': '1.0',
    'depends': ['base','mail','hr'],
    'application': True,
    'auto_install': False,
    'installable': True,
    'website': 'www.iza.com',
    'data': [
        'security/employee_transfer_user_group.xml',
        'security/ir.model.access.csv',
        'data/employee_transfer_sequence_data.xml',
        'views/employee_transfer_reject_view.xml',
        'views/employee_tansfer_approve_view.xml',
        'views/employee_transfer_waiting_approval_view.xml',
        'views/employee_transfer_draft_view.xml',
        'views/hr_employee_views.xml',
        'views/employee_transfer_view.xml',
        'views/employee_transfer_menu_view.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
