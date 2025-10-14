{
    'name': "Project Template",
    'version': '1.0',
    'summary': 'project templates',
    'description': 'projects and task templates',
    'author': 'ismail C A',
    'website': 'www.iza.com',

    'depends': ['base', 'project', ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_template_action_views.xml',
        'views/project_template_menu_views.xml',
        'views/project_template_button.xml'

    ],

    'installable': True,

    'application': True,
    'auto_install': False,

}
