# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class PlmStage(models.Model):
    _name = 'eco.stage'
    _description = 'ECO Stages'
    _fold_name = 'folded'
    _order = 'sequence, id'

    @api.model
    def _get_stage_sequence(self):
        stage = self.search([('sequence', '!=', False)], order='sequence desc', limit=1)
        if stage:
            return stage.sequence + 1

    name = fields.Char(string='Name', required=True)
    allow_apply_change = fields.Boolean()
    final_stage = fields.Boolean(copy=False)
    folded = fields.Boolean(copy=False, string="Folded in kanban view")
    sequence = fields.Integer(string='Sequence', default=_get_stage_sequence)
    eco_type_ids = fields.Many2many(
        'eco.type', 'eco_stage_type_rel', 'stage_id', 'eco_type_id', string='ECO types', required=True)
    approval_line_ids = fields.One2many(
        'stage.approval.line', 'stage_id', string='Approvals')
