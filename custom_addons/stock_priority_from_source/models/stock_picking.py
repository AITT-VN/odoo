from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # extend the existing priority field to include 'urgent'
    priority = fields.Selection(
        selection_add=[("urgent", "Urgent")],
        ondelete={"urgent": "set default"},
    )

    @api.model
    def create(self, vals):
        picking = super(StockPicking, self).create(vals)
        # Identify 3-step pickings whose names start with PICK or PACK
        # (e.g. PICK/0001, PACK/0001) :contentReference[oaicite:1]{index=1}
        name_prefix = picking.name.split("/", 1)[0] if picking.name else False
        if name_prefix in ("PICK", "PACK"):
            origin = picking.origin
            if origin:
                # find the Sale Order by its name
                sale = self.env["sale.order"].search([("name", "=", origin)], limit=1)
                # replace 'MySourceName' with the exact Source value you care about
                if sale and sale.source_id and sale.source_id.name == "MySourceName":
                    picking.write({"priority": "urgent"})
        return picking
