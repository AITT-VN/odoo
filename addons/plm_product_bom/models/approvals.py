# -*- coding: utf-8 -*-
from odoo import models, fields, _


class StageApproval(models.Model):
    _name = 'stage.approval.line'
    _description = 'Stage Approvals'

    name = fields.Char(string='Role', required=True)
    user_ids = fields.Many2many('res.users', string='Users', required=True)
    approval_type = fields.Selection([
        ('optional', 'Approves, but the approval is optional'),
        ('required', 'Is required to approve'),
    ],
        required=True, default="required")
    stage_id = fields.Many2one('eco.stage')


class EcoApprovals(models.Model):
    _name = 'eco.approval.line'
    _description = 'ECO Approvals'

    name = fields.Char(string='Role', required=True)
    user_id = fields.Many2one('res.users', string='Approved by')
    state = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('not_yet', 'Not Yet')],
        required=True, string="Status", default="not_yet")
    approval_datetime = fields.Datetime(string="Approval Date")
    stage_id = fields.Many2one('eco.stage', string="Stage")
    eco_id = fields.Many2one('plm.eco')
    approval_user_ids = fields.Many2many('res.users', string='Users')
    approval_type = fields.Selection([
        ('optional', 'Approves, but the approval is optional'),
        ('required', 'Is required to approve'),
    ])
