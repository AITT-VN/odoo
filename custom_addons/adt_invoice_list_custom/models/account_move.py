from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_paid = fields.Monetary(
        string="Amount Paid",
        compute="_compute_amount_paid",
        store=True,
        currency_field="currency_id",
    )

    payment_date_display = fields.Date(
        string="Payment Date",
        compute="_compute_last_payment_info",
        store=True,
    )

    recipient_bank_account_display = fields.Char(
        string="Recipient Bank Account",
        compute="_compute_last_payment_info",
        store=True,
    )

    @api.depends("amount_total", "amount_residual")
    def _compute_amount_paid(self):
        for record in self:
            record.amount_paid = record.amount_total - record.amount_residual

    @api.depends("invoice_payments_widget")
    def _compute_last_payment_info(self):
        """
        Compute the date and bank account from the latest payment.
        This method relies on the invoice_payments_widget, which is the standard
        way Odoo gets payment info for the invoice form.
        """
        for move in self:
            # Default values
            move.payment_date_display = False
            move.recipient_bank_account_display = ""

            # Get payment info from the widget
            payment_widget_info = move.invoice_payments_widget
            if not payment_widget_info or not payment_widget_info.get("content"):
                continue

            # Sort payments by date to find the most recent one
            sorted_payments = sorted(
                payment_widget_info["content"], key=lambda p: p["date"], reverse=True
            )

            if sorted_payments:
                last_payment = sorted_payments[0]
                payment_id = self.env["account.payment"].browse(
                    last_payment.get("account_payment_id")
                )
                if payment_id:
                    move.payment_date_display = payment_id.date
                    if payment_id.partner_bank_id:
                        move.recipient_bank_account_display = (
                            payment_id.partner_bank_id.display_name
                        )
