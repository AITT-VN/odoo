{
    'name': "Sale Order Phone and Mobile",
    'summary': """
        Adds Phone and Mobile fields from customer to Sale Order form.
    """,
    'description': """
        This module adds related fields for customer's phone and mobile numbers
        to the Sale Order form view, making them visible for quick reference.
    """,
    'author': "Your Name/Company", # Thay thế bằng tên của bạn
    'website': "http://www.yourcompany.com", # Thay thế bằng website của bạn (nếu có)
    'category': 'Sales',
    'version': '1.0',
    'depends': ['sale'], # Module này phụ thuộc vào module Sale cơ bản
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}