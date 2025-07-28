# -*- coding: utf-8 -*-
{
    'name': "QC Project",
    'summary': "Module for managing Quality Control projects",
    'description': """
        Module for managing employees and quality control projects.
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Quality Control',
    'version': '0.1',
    'depends': ['base','web','project', 'mail', 'hr'],
    'data': [
        'security/qc_project_security.xml',
        'data/practice_data.xml',  # Ajoutez ici
        'views/qcproject_actions.xml',
        'views/qcproject_menus.xml',
        'views/qcproject_employee_view.xml',
        'views/hr_department_view.xml',
        'views/qcproject_project_view.xml',
        'views/qcproject_skill_view.xml',
        'views/qcproject_task_view.xml',
        'views/qcproject_sub_task_view.xml',
        'views/qcproject_tag_views.xml',
        'views/qcproject_project_delivery_view.xml',
        'views/qcproject_workflow.xml',
        'views/work_program_view.xml',
        'views/project_views.xml',


        'views/views.xml',
        # 'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'qcproject/static/css/fix_kanban.scss',
            'qcproject/static/css/employee_styles.css',
            'qcproject/static/js/employee_scripts.js',
            'qcproject/static/css/employee_page.css',
        ],
        'web.assets_common': [
            # Optional: Add if hosting Animate.css locally
            # 'qctracker/static/src/css/animate.min.css',
        ],
    },
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}