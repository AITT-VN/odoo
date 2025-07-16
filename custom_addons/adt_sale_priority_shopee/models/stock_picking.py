from odoo import models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        for picking in pickings:
            # 1. Nếu đơn này là pick được tạo từ đơn hàng Shopee → đánh sao
            if picking.origin:
                sale_order = self.env["sale.order"].search(
                    [("name", "=", picking.origin)], limit=1
                )
                if (
                    sale_order
                    and sale_order.source_id
                    and sale_order.source_id.name.strip().lower() == "shopee"
                ):
                    picking.priority = "1"  # Gán sao vàng

            # 2. Nếu đơn này là Pack hoặc Delivery và đơn Pick cùng group có sao → kế thừa sao
            if not picking.priority or picking.priority == "0":
                related_pickings = self.env["stock.picking"].search(
                    [
                        ("group_id", "=", picking.group_id.id),
                        ("priority", "=", "1"),
                        ("id", "!=", picking.id),
                    ]
                )
                if related_pickings:
                    picking.priority = "1"
        return pickings
