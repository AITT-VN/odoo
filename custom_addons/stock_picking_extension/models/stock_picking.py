from odoo import models, fields, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_street = fields.Char(
        related='partner_id.street',
        string=_('Address'),
        readonly=True
    )
    partner_phone = fields.Char(
        related='partner_id.phone',
        string=_('Phone'),
        readonly=True
    )
    partner_mobile = fields.Char(
        related='partner_id.mobile',
        string=_('Mobile'),
        readonly=True
    )
