# -*- coding: utf-8 -*-
{
    'name': "project_expense",

    'summary': """
        My_Name : Ahmed Ashraf EL Naggar
        My_Whatsapp_number: +201122702847
        My_Gthup : https://github.com/ahmedashrafelnaggar?tab=repositories
        Email: www.ahmedashraf83@gmail.com
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Ahmed Ashraf ",
    'website': "https://github.com/ahmedashrafelnaggar?tab=repositories",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','mail', 'stock', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/project_view.xml',
        'views/expense_type_view.xml',
        'views/expense_request_view.xml',
        'views/base_menu.xml',
        'views/product_view.xml',
        'views/portal_templates.xml',
        'wizard/expense_report_wizard.xml',
        'reports/expense_request_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
