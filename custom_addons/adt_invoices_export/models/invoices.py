from odoo import models, fields
import io
from openpyxl import Workbook
from odoo.http import request


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def generate_export_out_invoice(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Invoices"

        headers = {
            "ngay_hach_toan": "Ngày hạch toán (*)",
            "ngay_chung_tu": "Ngày chứng từ (*)",
            "so_chung_tu": "Số chứng từ (*)",
            "ma_doi_tuong": "Mã đối tượng",
            "ten_doi_tuong": "Tên đối tượng",
            "nop_vao_tk": "Nộp vào TK",
            "mo_tai_ngan_hang": "Mở tại ngân hàng",
            "ly_do_thu": "Lý do thu",
            "dien_giai_ly_do_thu": "Diễn giải lý do thu",
            "loai_tien": "Loại tiền",
            "ty_gia": "Tỷ giá",
            "dien_giai_hach_toan": "Diễn giải (hạch toán)",
            "tk_no": "TK Nợ (*)",
            "tk_co": "TK Có (*)",
            "so_tien": "Số tiền",
            "quy_doi": "Quy đổi",
            "ma_doi_tuong_hach_toan": "Mã đối tượng (hạch toán)",
        }

        ws.append(list(headers.values()))

        # Filter only paid invoices
        paid_invoices = self.filtered(lambda invoice: invoice.payment_state == "paid")

        for invoice in paid_invoices:
            row = {}
            row["ngay_hach_toan"] = invoice.invoice_date.strftime("%d/%m/%Y")
            row["ngay_chung_tu"] = invoice.invoice_date.strftime("%d/%m/%Y")
            row["so_chung_tu"] = invoice.name
            row["ma_doi_tuong"] = (
                invoice.partner_id.ref if invoice.partner_id.ref else ""
            )
            row["ten_doi_tuong"] = invoice.partner_id.name

            partner_bank = invoice.partner_bank_id
            acc_number = partner_bank.acc_number if partner_bank else ""
            bank_name = partner_bank.bank_id.name if partner_bank else ""

            row["nop_vao_tk"] = acc_number
            row["mo_tai_ngan_hang"] = bank_name
            row["ly_do_thu"] = "Thu tiền khách hàng (không theo hóa đơn)"
            row["dien_giai_ly_do_thu"] = invoice.payment_reference
            row["loai_tien"] = "VND"
            row["ty_gia"] = 1
            row["dien_giai_hach_toan"] = invoice.payment_reference
            row["tk_no"] = 1121
            row["tk_co"] = 1311
            row["so_tien"] = invoice.amount_total
            row["quy_doi"] = row["so_tien"] * row["ty_gia"]
            row["ma_doi_tuong_hach_toan"] = (
                invoice.partner_id.ref if invoice.partner_id.ref else ""
            )

            row_values = [row.get(key, "") for key in headers.keys()]
            ws.append(row_values)

        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        return file_stream.read()

    def export_custom_out_invoice(self):
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        invoice_ids = ",".join(str(id) for id in self.ids)
        url = f"{base_url}/adt_invoices_export/export_out_invoice?invoice_ids={invoice_ids}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
