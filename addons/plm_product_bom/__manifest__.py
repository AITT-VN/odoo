# -*- coding: utf-8 -*-
{
    'name': "Product Lifecycle Management For Community",

    'summary': "ECO for products and bill of materials - Community",

    'description': """
        Manage engineering change orders on products and bill of materials for community edition
    """,

    'author': "Just Try",
    'version': '18.0.1.0.0',
    'website': "",
    'category': 'Manufacturing',
    'version': '0.1',
    'images': ['static/description/banner.png'],
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/stage_views.xml',
        'views/type_views.xml',
        'views/tag_views.xml',
        'views/plm_eco_views.xml',
        'views/product_template_views.xml',
        'views/plm_menuitem.xml',
    ],
    'price': 9,
    'currency': 'USD',
    'license': 'OPL-1',
    'application': True

}
