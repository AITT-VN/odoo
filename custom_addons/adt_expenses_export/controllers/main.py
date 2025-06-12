from odoo import http
from odoo.http import request
from datetime import datetime


class ExpenseExportController(http.Controller):

    @http.route("/adt_expenses_export/export_expense", type="http", auth="user")
    def export_expense(self, **kw):
        expense_ids = kw.get("expense_ids")
        if expense_ids:
            expense_ids = [int(i) for i in expense_ids.split(",")]
            expenses = request.env["hr.expense"].sudo().browse(expense_ids)
        else:
            expenses = request.env["hr.expense"].sudo().search([])

        file_content = expenses.generate_export_expenses()

        filename = f"Chi Phi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        headers = [
            (
                "Content-Type",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            ("Content-Disposition", f'attachment; filename="{filename}"'),
            ("Content-Length", len(file_content)),
        ]

        return request.make_response(file_content, headers)
