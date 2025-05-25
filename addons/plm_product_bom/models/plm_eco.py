# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class PlmEco(models.Model):
    _name = 'plm.eco'
    _inherit = ['mail.thread']
    _description = 'PLM ECO'

    name = fields.Char(string='Reference', required=True)
    eco_type_id = fields.Many2one('eco.type', string="Type", required=True)
    apply_type = fields.Selection([
        ('product', 'Product'),
        ('bom', 'Bill of Material'),
    ],
        required=True, default="product")
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, required=True, readonly=True)
    product_tmpl_id = fields.Many2one(
        'product.template', required=True, ondelete='cascade', check_company=True, string='Product')
    bom_id = fields.Many2one('mrp.bom', 'BOM', ondelete='cascade',
                             domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    new_bom_id = fields.Many2one('mrp.bom', 'BOM', ondelete='cascade')
    user_id = fields.Many2one(
        'res.users', string='Responsible', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('eco.tag')
    note = fields.Html()
    stage_id = fields.Many2one('eco.stage', string="Stage", copy=False, tracking=True,
                               domain="[('eco_type_ids', 'in', eco_type_id)]",
                               group_expand="_read_group_stage_ids")
    state = fields.Selection([
        ('new', 'New'),
        ('progress', 'In Progress'),
        ('done', 'Done')
    ],
        required=True, default="new", readonly=True, copy=False, string="Status")
    approval_line_ids = fields.One2many(
        'eco.approval.line', 'eco_id', string="Approvals")
    can_approve = fields.Boolean(compute="_user_can_approve_eco")
    user_last_action = fields.Selection([
        ('not_yet', 'Not Yet'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')], copy=False, default="not_yet", compute="_compute_last_action")
    stage_apply_changes = fields.Boolean(related='stage_id.allow_apply_change')

    bom_change_line_ids = fields.One2many('plm.eco.bom.change.line', 'eco_id')

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        """ display all stages in the kanban view
        """
        search_domain = []
        if 'default_eco_type_id' in self.env.context:
            search_domain = [('eco_type_ids', '=', self.env.context['default_eco_type_id'])]
        stage_ids = stages.sudo()._search(search_domain, order=stages._order)
        return stages.browse(stage_ids)

    @api.onchange('eco_type_id')
    def onchange_eco_type_id(self):
        self.stage_id = self.env['eco.stage'].search(
            [('eco_type_ids', 'in', self.eco_type_id.id)], limit=1).id

    @api.depends_context('uid')
    @api.depends('approval_line_ids', 'approval_line_ids.state')
    def _compute_last_action(self):
        for eco in self:
            user_last_approval = eco.approval_line_ids.filtered(
                lambda l: self.env.user == l.user_id and l.stage_id == self.stage_id).sorted(key=lambda l: l.id)
            if user_last_approval:
                eco.user_last_action = user_last_approval[-1].state
            else:
                eco.user_last_action = 'not_yet'

    @api.depends_context('uid')
    @api.depends('stage_id', 'stage_id.approval_line_ids')
    def _user_can_approve_eco(self):
        for eco in self:
            approvals = eco.stage_id.approval_line_ids.filtered(
                lambda l: self.env.user in l.user_ids)
            eco.can_approve = True if approvals else False

    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals:
            if vals['stage_id']:
                stage_id = vals['stage_id']
                if int(stage_id) not in self.eco_type_id.stage_ids.ids:
                    raise UserError(
                        _("You cannot move ECO to this stage, doesn't belong to the same ECO type."))
                self._check_stage_changes()
                stage_approvals = self.stage_id.approval_line_ids
                eco_approvals = self.approval_line_ids
                if stage_approvals and not eco_approvals.filtered(lambda l: l.stage_id == self.stage_id):
                    self._auto_add_approvals()
        return res

    def action_revision(self):
        if self.bom_id and not self.new_bom_id:
            self.new_bom_id = self.bom_id.sudo().copy(default={
                'version': self.bom_id.version + 1,
                'active': False
            })
        self.state = 'progress'

    def apply_changes(self):
        for eco in self:
            eco._check_apply_changes()
            if eco.apply_type == 'product':
                eco.product_tmpl_id.version += 1
            elif eco.apply_type == 'bom':
                eco.bom_id.write({
                    'active': False
                })
                eco.new_bom_id.write({
                    'active': True
                })
                eco.add_bom_changes()
            final_stage = eco.eco_type_id.stage_ids.filtered(
                lambda l: l.final_stage).sorted(lambda l: l.sequence)[-1]
            if final_stage:
                eco.stage_id = final_stage
            eco.state = 'done'

    def _check_stage_changes(self):
        stage = self._origin
        if stage:
            approval_lines = []
            eco_approval_lines = stage.approval_line_ids._read_group(
                domain=[('eco_id', '=', stage.id),
                        ('approval_type', '=', 'required')],
                groupby=['user_id'],
                aggregates=['id:recordset']
            )
            
            #  Check if any line needs approval // for this stage.
            
            for user, record in eco_approval_lines:
                if record[-1] and record[-1].state != 'approved':
                    raise UserError(
                        _("You cannot change the stage, as approvals are still required."))

            #  Check if any upcoming stage needs approval.
            
            need_approve = []
            stages = stage.eco_type_id.stage_ids.filtered(
                lambda s: s.sequence > stage.stage_id.sequence and s.sequence < self.stage_id.sequence)
            for stage in stages:
                if stage.approval_line_ids.filtered(lambda l: l.approval_type == 'required'):
                    need_approve.append(stage.name)
            if need_approve:
                raise UserError(
                    _("You cannot change the stage/s to %s, as approvals are still required.", need_approve))

    def _check_apply_changes(self):
        approval_lines = []
        eco_approval_lines = self.approval_line_ids._read_group(
            domain=[('eco_id', '=', self.id),
                    ('approval_type', '=', 'required')],
            groupby=['user_id'],
            aggregates=['id:recordset']
        )
        
        #  Check if any line needs approval // for this stage.
        
        for user, record in eco_approval_lines:
            if record[-1] and record[-1].state != 'approved':
                raise UserError(
                    _("You cannot change the stage, as approvals are still required."))

        #  Check if any upcoming stage needs approval.
        
        need_approve = []
        stages = self.eco_type_id.stage_ids.filtered(
            lambda s: s.sequence > self.stage_id.sequence)
        for stage in stages:
            if stage.approval_line_ids.filtered(lambda l: l.approval_type == 'required'):
                need_approve.append(stage.name)
        if need_approve:
            raise UserError(
                _("You cannot change the stage/s to %s, as approvals are still required.", need_approve))

    def action_new_bom(self):
        self.ensure_one()
        return {
            'name': _('ECO BOM'),
            'res_model': 'mrp.bom',
            'res_id': self.new_bom_id.id,
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    def action_approve(self):
        approvals = self.approval_line_ids.filtered(
            lambda l: self.env.user in l.approval_user_ids and l.state == 'not_yet')
        for approval in approvals:
            approval.write({
                'approval_datetime': datetime.now(),
                'state': 'approved',
                'user_id': self.env.user,
                'approval_type': approval.approval_type
            })
        if not approvals:
            self._auto_add_approvals(state='approved', user=self.env.user)
        # self.user_last_action = 'approved'

    def action_reject(self):
        approvals = self.approval_line_ids.filtered(
            lambda l: self.env.user in l.approval_user_ids and l.state == 'not_yet')
        for approval in approvals:
            approval.write({
                'approval_datetime': datetime.now(),
                'state': 'rejected',
                'user_id': self.env.user,
                'approval_type': approval.approval_type
            })
        if not approvals:
            self._auto_add_approvals(state='rejected', user=self.env.user)

    def _auto_add_approvals(self, state=False, user=False):
        line_ids = []
        stage_approvals = self.stage_id.approval_line_ids.filtered(
            lambda l: self.env.user in l.user_ids) if user else self.stage_id.approval_line_ids
        for approval in stage_approvals:
            vals = {
                'approval_user_ids': approval.user_ids,
                'approval_type': approval.approval_type,
                'name': approval.name,
                'stage_id': self.stage_id.id,
            }
            if user and state:
                vals['state'] = state
                vals['approval_datetime'] = datetime.now()
                vals['user_id'] = user.id
                vals['approval_type'] = approval.approval_type
            line_ids.append((0, 0, vals))
        self.update({
            'approval_line_ids': line_ids
        })

    def add_bom_changes(self):
        old_bom_components = self.bom_id.bom_line_ids
        new_bom_components = self.new_bom_id.bom_line_ids
        values = []
        shared = set(old_bom_components.product_id.ids) & set(new_bom_components.product_id.ids) 
        removed_lines = set(old_bom_components.product_id.ids) - set(new_bom_components.product_id.ids) 
        added_lines = set(new_bom_components.product_id.ids) - set(old_bom_components.product_id.ids) 

        for product_id in shared:
            old_line = old_bom_components.filtered(lambda l: l.product_id.id == product_id)
            new_line = new_bom_components.filtered(lambda l: l.product_id.id == product_id)
            quantity = new_line.product_qty - old_line.product_qty
            if quantity != 0:
                vals = {
                    'product_id': product_id,
                    'action_type': 'update_add' if quantity > 0 else 'update_remove',
                    'quantity': abs(quantity)
                }
                values.append((0, 0, vals))

        for product_id in added_lines:
            new_line = new_bom_components.filtered(lambda l: l.product_id.id == product_id)
            vals={
                'product_id': new_line.product_id.id,
                'action_type': 'add',
                'quantity': new_line.product_qty
            }
            values.append((0, 0, vals))

        for product_id in removed_lines:
            old_line = old_bom_components.filtered(lambda l: l.product_id.id == product_id)
            vals={
                'product_id': old_line.product_id.id,
                'action_type': 'remove',
                'quantity': old_line.product_qty
            }
            values.append((0, 0, vals))
        self.update({
            'bom_change_line_ids': values
        })

class PlmEcoBomChanges(models.Model):
    _name = 'plm.eco.bom.change.line'
    _description = 'PLM ECO BOM Change Line'

    product_id = fields.Many2one('product.product', 'Component') 
    quantity = fields.Float('Quantity') 
    action_type = fields.Selection([
        ('update_add', 'Update/Add'),
        ('update_remove', 'Update/Remove'),
        ('add', 'Add'),
        ('remove', 'Remove'),
    ])

    eco_id = fields.Many2one('plm.eco')
