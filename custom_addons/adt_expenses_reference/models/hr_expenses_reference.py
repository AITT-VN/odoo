from odoo import models, fields, api

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    expense_code = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Không tạo lại mã nếu đã có
            if not vals.get('expense_code') or vals['expense_code'] == 'New':
                vals['expense_code'] = self.env['ir.sequence'].next_by_code('hr.expense.reference')
        return super().create(vals_list)





