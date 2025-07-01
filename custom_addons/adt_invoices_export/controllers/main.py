from odoo import http
from odoo.http import request
from datetime import datetime

class InvoiceExportController(http.Controller):

    @http.route('/adt_invoices_export/export_out_invoice', type='http', auth="user")
    def export_out_invoices(self, **kw):
        invoice_ids = kw.get('invoice_ids')
        if invoice_ids:
            invoice_ids = [int(i) for i in invoice_ids.split(',')]
            invoices = request.env['account.move'].sudo().browse(invoice_ids)
        else:
            invoices = request.env['account.move'].sudo().search([])

        file_content = invoices.generate_export_out_invoice()

        filename = f"Hoa Don Ban Hang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        headers = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
            ('Content-Length', len(file_content)),
        ]

        return request.make_response(file_content, headers)
