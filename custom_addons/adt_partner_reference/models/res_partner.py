from odoo import api, fields, models
from datetime import datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    ref = fields.Char(
        string="Reference",
        copy=False,
        default=lambda self: (
            "OHC{}{}".format(
                datetime.now().strftime("%Y%m%d%H%M"),
                self.env["ir.sequence"].next_by_code("partner.ref.counter"),
            )
        ),
        help="Unique MISA partner reference generated automatically.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        When new partners are created (even in batch/imports), if 'ref' was not explicitly given
        in vals, assign the next value from ir.sequence('partner.ref').
        """
        for vals in vals_list:
            # If the user did not supply a 'ref' manually, fetch from the sequence:
            if not vals.get("ref"):
                ts = datetime.now().strftime("%Y%m%d%H%M")
                tail = self.env["ir.sequence"].next_by_code("partner.ref.counter")
                vals["ref"] = f"OHC{ts}{tail}"
        return super(ResPartner, self).create(vals_list)
