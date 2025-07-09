from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    recipient_bank_id = fields.Many2one("res.bank", string="Recipient Bank")

    amount_paid = fields.Monetary(
        string="Amount Paid",
        compute="_compute_amount_paid",
        store=True,
        currency_field="currency_id",
    )

    @api.depends("amount_total", "amount_residual")
    def _compute_amount_paid(self):
        for record in self:
            record.amount_paid = record.amount_total - record.amount_residual
