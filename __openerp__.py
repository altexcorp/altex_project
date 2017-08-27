# -*- coding: utf-8 -*-
{
    'name': "Altex Project",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Altex-corp",
    'website': "http://altex-corp.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Project',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'views/project_view.xml',
        'wizard/customer_timesheet_view.xml',
        'data/sequence.xml',
        'data/project_state.xml',
        'report/project_report.xml',
        'report/customer_timesheet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'installable': True,
}
