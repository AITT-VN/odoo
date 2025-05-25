# -*- coding: utf-8 -*-
from odoo import models, fields, _
from random import randint


class PlmTag(models.Model):
    _name = 'eco.tag'
    _description = 'ECO Tags'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)
