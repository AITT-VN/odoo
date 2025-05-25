# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    version = fields.Integer(copy=False, readonly=True, default=1)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    version = fields.Integer(copy=False, readonly=True, default=1)
