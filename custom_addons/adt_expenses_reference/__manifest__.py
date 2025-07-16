{
    "name": "ADT Expenses Reference Generation",
    "version": "18.0.1.0.0",
    "summary": "Tự động sinh mã khi tạo mới expense",
    "author": "TrucHa",
    "category": "Accounting",
    "depends": ["hr_expense"],
    "data": [
        "data/auto_reference_sequence.xml",
        "views/expenses_reference_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
