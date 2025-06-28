from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_phone = fields.Char(
        related='partner_id.phone',
        string='Phone',
        readonly=True
    )

    partner_mobile = fields.Char(
        related='partner_id.mobile',
        string='Mobile',
        readonly=True
    )