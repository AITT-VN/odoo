# -*- coding: utf-8 -*-
from odoo import models, fields, _


class PlmType(models.Model):
    _name = 'eco.type'
    _description = 'ECO Types'

    name = fields.Char(string='Name', required=True)
    stage_ids = fields.Many2many(
        'eco.stage', 'eco_stage_type_rel', 'eco_type_id', 'stage_id', string='ECO Stages')
    eco_count = fields.Integer(string="ECO Count", compute="_compute_eco_count")

    def open_eco_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("plm_product_bom.eco_action")
        action['domain'] = [('eco_type_id', '=', self.id)]
        action['context'] = {'default_eco_type_id': self.id}
        return action

    def _compute_eco_count(self):
        eco_data = self.env['plm.eco']._read_group([('eco_type_id', 'in', self.ids), (
            'stage_id.final_stage', '!=', True)], ['eco_type_id'], ['__count'])
        mapping = {eco.id: count for eco, count in eco_data}
        for eco in self:
            eco.eco_count = mapping.get(eco.id, 0)
