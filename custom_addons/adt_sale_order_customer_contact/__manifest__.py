{
    'name': 'ADT Sale Order Customer Contact',
    'version': '1.3',
    'summary': 'Show customer phone and mobile in sales order for ADT',
    'author': 'ADT',
    'category': 'Sales',
    'depends': ['sale', 'contacts'],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_order_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}
