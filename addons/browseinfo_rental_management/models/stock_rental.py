# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api,  models, _, fields
from datetime import datetime
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.tools import float_compare, float_round, float_is_zero, OrderedSet, DEFAULT_SERVER_DATETIME_FORMAT


class Picking(models.Model):
    _inherit = 'stock.picking'

    def action_cancel_draft(self):
        if not len(self.ids):
            return False
        move_obj = self.env['stock.move']
        for (ids, name) in self._compute_display_name():
            message = _("Picking '%s' has been set in draft state.") % name
            self.message_post(message)
        for pick in self:
            ids2 = [move.id for move in pick.move_ids]
            moves = move_obj.browse(ids2)
            moves.sudo().action_draft()
        return True


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def action_cancel_quant_create(self):
        quant_obj = self.env['stock.quant']
        for move in self:
            price_unit = move.get_price_unit()
            location = move.location_id
            rounding = move.product_id.uom_id.rounding
            vals = {
                'product_id': move.product_id.id,
                'location_id': location.id,
                'qty': float_round(move.product_uom_qty, precision_rounding=rounding),
                'cost': price_unit,
                'in_date': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'company_id': move.company_id.id,
            }
            quant_obj.sudo().create(vals)
            return
        
    def action_draft(self):
        res = self.write({'state': 'draft'})
        return res


    def _do_unreserve(self):
        rental_details = self.env['ir.config_parameter'].sudo().get_param('browseinfo_rental_management.saleable_rental_details')
        moves_to_unreserve = OrderedSet()
        for move in self:
            # if rental_details:
            #     # move.move_line_ids.unlink()
            #     if move.procure_method == 'make_to_order' and not move.move_orig_ids:
            #         move.state = 'waiting'
            #     elif move.move_orig_ids and not all(orig.state in ('done', 'cancel') for orig in move.move_orig_ids):
            #         move.state = 'waiting'
            #     else:
            #         move.state = 'confirmed'

            # else
            if move.state == 'cancel' or (move.state == 'done' and move.scrapped) or move.picked:
                # We may have cancelled move in an open picking in a "propagate_cancel" scenario.
                # We may have done move in an open picking in a scrap scenario.
                continue
            elif move.state == 'done':
                raise UserError(_("You cannot unreserve a stock move that has been set to 'Done'."))
            moves_to_unreserve.add(move.id)
            moves_to_unreserve = self.env['stock.move'].browse(moves_to_unreserve)

            ml_to_unlink = OrderedSet()
            moves_not_to_recompute = OrderedSet()
            for ml in moves_to_unreserve.move_line_ids:
                if ml.picked:
                    moves_not_to_recompute.add(ml.move_id.id)
                    continue
                ml_to_unlink.add(ml.id)
            ml_to_unlink = self.env['stock.move.line'].browse(ml_to_unlink)
            moves_not_to_recompute = self.env['stock.move'].browse(moves_not_to_recompute)

            ml_to_unlink.unlink()
            # `write` on `stock.move.line` doesn't call `_recompute_state` (unlike to `unlink`),
            # so it must be called for each move where no move line has been deleted.
            (moves_to_unreserve - moves_not_to_recompute)._recompute_state()
        return True


    def _action_cancel(self):
        for move in self:
            move._do_unreserve()
            siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
            if move.propagate_cancel:
                if all(state == 'cancel' for state in siblings_states):
                    move.move_dest_ids._action_cancel()
            else:
                if all(state in ('done', 'cancel') for state in siblings_states):
                    move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                    move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
        
            if move.picking_id.state == 'done' or 'confirmed':
                pack_op = self.env['stock.move'].sudo().search([('picking_id','=',move.picking_id.id),('product_id','=',move.product_id.id)])
                for pack_op_id in pack_op:
                    if move.picking_id.picking_type_id.code in ['outgoing','internal']:
                        for move_id in pack_op:
                            for line in move_id.move_line_ids:
                                if line.lot_id:
                                    lot_outgoing_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',line.location_dest_id.id),('lot_id','=',line.lot_id.id)])
                                    lot_source_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',line.location_id.id),('lot_id','=',line.lot_id.id)])
                                    if lot_outgoing_quant.product_id.tracking == 'lot'or lot_source_quant.product_id.tracking == 'lot':
                                        if lot_outgoing_quant:
                                            for lot in lot_outgoing_quant:
                                                old_qty = lot.quantity
                                                lot.quantity = old_qty - move.product_uom_qty
                                        if lot_source_quant:
                                            for lot in lot_source_quant:
                                                old_qty = lot.quantity
                                                lot.quantity = old_qty + move.product_uom_qty
                                        else:
                                            vals = { 'product_id' :move.product_id.id,
                                                    'location_id':move.location_id.id,
                                                    'lot_id':line.lot_id.id,
                                                    'quantity':move.product_uom_qty,
                                                }
                                            self.env['stock.quant'].create(vals)
                                    else:
                                        if lot_outgoing_quant:
                                            for lot in lot_outgoing_quant:
                                                old_qty = lot.quantity
                                                lot.unlink()
                                                vals = { 'product_id' :move.product_id.id,
                                                        'location_id':move.location_id.id,
                                                        'quantity': old_qty,
                                                        'lot_id':line.lot_id.id,
                                                    }
                                                test = self.env['stock.quant'].create(vals)
                                            
                                else:
                                    if pack_op_id.location_dest_id.usage == 'customer':
                                        outgoing_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_dest_id.id)])
                                        stock_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_id.id)])
                                        if outgoing_quant:
                                            old_qty = outgoing_quant[0].quantity
                                            outgoing_quant[0].quantity = old_qty - move.product_uom_qty
                                        if stock_quant:
                                            old_qty = stock_quant[0].quantity
                                            stock_quant[0].quantity = old_qty + move.product_uom_qty
                                    else:
                                        outgoing_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_id.id)])
                                        if outgoing_quant:
                                            old_qty = outgoing_quant[0].quantity
                                            outgoing_quant[0].quantity = old_qty + move.product_uom_qty
                                        outgoing_customer_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_dest_id.id)])
                                        if outgoing_customer_quant:
                                            old_qty = outgoing_quant[0].quantity
                                            outgoing_quant[0].quantity = old_qty - move.product_uom_qty

                    if move.picking_id.picking_type_id.code == 'incoming':
                        incoming_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_dest_id.id)])
                        if incoming_quant:
                            old_qty = incoming_quant[0].quantity
                            incoming_quant[0].quantity = old_qty - move.product_uom_qty
                        incoming_customer_quant = self.env['stock.quant'].sudo().search([('product_id','=',move.product_id.id),('location_id','=',pack_op_id.location_id.id)])
                        if incoming_customer_quant:
                            old_qty = incoming_customer_quant[0].quantity
                            incoming_customer_quant[0].quantity = old_qty + move.product_uom_qty
                    
            self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})        
        return True

class stock_move_line(models.Model):
    _inherit = "stock.move.line"

    replaced_ = fields.Boolean(string="Replaced")
    
    def unlink(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for ml in self:
            if ml.product_id.type == 'product' and not ml.location_id.should_bypass_reservation() and not float_is_zero(ml.product_packaging_qty, precision_digits=precision):
                quant = self.env['stock.quant']._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty, lot_id=ml.lot_id,
                                                                   package_id=ml.package_id, owner_id=ml.owner_id, strict=True)
        return super(stock_move_line, self).unlink()