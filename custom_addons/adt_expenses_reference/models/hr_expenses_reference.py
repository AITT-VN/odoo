from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = "hr.expense"

    expense_ref = fields.Char(
        string="Reference", required=True, readonly=True, copy=False, default="New"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Không tạo lại mã nếu đã có
            if not vals.get("expense_ref") or vals["expense_ref"] == "New":
                vals["expense_ref"] = self.env["ir.sequence"].next_by_code(
                    "hr.expense.reference"
                )
        return super().create(vals_list)
