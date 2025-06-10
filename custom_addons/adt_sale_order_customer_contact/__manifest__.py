{
    'name': 'ADT Sales Orders Customization',
    'version': '1.3',
    'summary': 'Thêm thông tin Số điện thoại trên trang Đơn bán hàng',
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
