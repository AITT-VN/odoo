from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_phone = fields.Char(string=_('Phone'), related='partner_id.phone', readonly=True)
    partner_mobile = fields.Char(string=_('Mobile'), related='partner_id.mobile', readonly=True)
