from odoo import http
from odoo.http import request
from datetime import datetime

class SaleOrderExportController(http.Controller):

    @http.route('/adt_sale_order_export/export_excel', type='http', auth='user')
    def export_excel(self, **kw):
        order_ids = kw.get('order_ids')
        if order_ids:
            order_ids = [int(i) for i in order_ids.split(',')]
            orders = request.env['sale.order'].sudo().browse(order_ids)
        else:
            orders = request.env['sale.order'].sudo().search([])

        file_content = orders.generate_export_excel()

        filename = f"Don Ban Hang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        headers = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
            ('Content-Length', len(file_content)),
        ]

        return request.make_response(file_content, headers)
