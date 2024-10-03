# -*- coding: utf-8 -*-
{
    'name': "booking_order_ADHITIA_ZAIN_02102024",

    'author': "Adhitia Zain Nurrizki",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',
        'views/service_team_view.xml',
        'views/work_order_view.xml',
        'data/sequence_data.xml',
        'views/menu_views.xml',
        # 'report/report_work_order.xml',
        # 'report/report_work_order_action.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}