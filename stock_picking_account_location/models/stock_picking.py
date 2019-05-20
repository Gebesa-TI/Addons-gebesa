# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def picking_account_move_generate(self, move, credit_account_id,
                                      debit_account_id, journal_id):
        quant_obj = self.env['stock.quant']
        move_obj = self.env['account.move']
        if move.location_id.usage == 'production' and \
                move.location_dest_id.usage == 'production':
            return

        reference = False
        if move.picking_id:
            reference = move.picking_id.name or False
        elif move.production_id:
            reference = move.production_id.name or False
        elif move.raw_material_production_id:
            reference = move.raw_material_production_id.name or False
        elif move.inventory_id:
            reference = move.name or False
        else:
            reference = "W/O Reference"

        cost = move.get_price_unit(move)
        qty = move.product_uom_qty

        move_lines = quant_obj._prepare_account_move_line(
            move, qty, cost, credit_account_id,
            debit_account_id)

        date = self._context.get('force_period_date',
                                 fields.datetime.now()
                                 )
        new_move = move_obj.create({
            'journal_id': journal_id,
            'line_ids': move_lines,
            'date': date,
            'ref': reference
        })
        new_move.post()
        move.acc_move_id = new_move

    @api.multi
    def picking_prepare_account_move(self):
        quant_obj = self.env['stock.quant']
        for pick in self:
            move_ids = []
            for move in pick.move_lines:
                import ipdb; ipdb.set_trace()
                if move.state != 'done':
                    continue
                location_from = move.location_id
                location_to = move.location_dest_id
                company_from = location_from._location_owner(location_from)
                company_to = location_to._location_owner(location_to)

                if move.product_id.valuation != 'real_time':
                    continue

                if move.product_uom_qty <= 0:
                    continue

                if company_to and (move.location_id.type_stock_loc != 'rm' and
                                   move.location_dest_id.type_stock_loc == 'rm' or
                                   move.location_id.type_stock_loc != 'fp' and
                                   move.location_dest_id.type_stock_loc == 'fp' or
                                   company_from != company_to):
                    ctx = self._context.copy()
                    ctx['force_company'] = company_to.id
                    journal_id, acc_src, acc_dest, acc_valuation = \
                        quant_obj._get_accounting_data_for_valuation(move)
                    if location_to and location_to.usage == 'supplier':
                        self.picking_account_move_generate(
                            move, acc_dest, acc_valuation, journal_id)
                    else:
                        self.picking_account_move_generate(
                            move, acc_src, acc_valuation, journal_id)

                if company_from and (move.location_id.type_stock_loc == 'rm' and
                                     move.location_dest_id.type_stock_loc != 'rm' or
                                     move.location_id.type_stock_loc == 'fp' and
                                     move.location_dest_id.type_stock_loc != 'fp' or
                                     company_from != company_to):
                    ctx = self._context.copy()
                    ctx['force_company'] = company_from.id
                    journal_id, acc_src, acc_dest, acc_valuation = \
                        quant_obj._get_accounting_data_for_valuation(move)
                    if location_to and location_to.usage == 'supplier':
                        self.picking_account_move_generate(
                            move, acc_valuation, acc_src, journal_id)
                    else:
                        self.picking_account_move_generate(
                            move, acc_valuation, acc_dest, journal_id)

                if move.company_id.anglo_saxon_accounting and \
                        move.location_id.usage == 'supplier' and \
                        move.location_dest_id.usage == 'customer':
                    ctx = self._context.copy()
                    ctx['force_company'] = move.company_id.id
                    journal_id, acc_src, acc_dest, acc_valuation = \
                        quant_obj._get_accounting_data_for_valuation(move)
                    self.picking_account_move_generate(
                        move, acc_src, acc_dest, journal_id)

                if move.location_id.usage == 'internal' and \
                        move.location_dest_id.usage == 'internal' and \
                        move.location_id.stock_warehouse_id.id != \
                        move.location_dest_id.stock_warehouse_id.id:
                    ctx = self._context.copy()
                    ctx['force_company'] = move.company_id.id
                    journal_id, acc_src, acc_dest, acc_valuation = \
                        quant_obj._get_accounting_data_for_valuation(move)
                    self.picking_account_move_generate(
                        move, acc_src, acc_dest, journal_id)

                if move.location_id.usage == 'transit' and  \
                        move.location_dest_id.usage == 'production':
                    ctx = self._context.copy()
                    ctx['force_company'] = move.company_id.id
                    journal_id, acc_src, acc_dest, acc_valuation =  \
                        quant_obj._get_accounting_data_for_valuation(move)
                    self.picking_account_move_generate(
                        move, acc_src, acc_dest, journal_id)

                if move.location_id.type_stock_loc == 'wip' and \
                        move.location_dest_id.usage == 'transit':
                    ctx = self._context.copy()
                    ctx['force_company'] = move.company_id.id
                    journal_id, acc_src, acc_dest, acc_valuation =  \
                        quant_obj._get_accounting_data_for_valuation(move)
                    self.picking_account_move_generate(
                        move, acc_src, acc_dest, journal_id)

                if (move.location_id.type_stock_loc == 'wip' and
                        move.location_dest_id.usage == 'inventory') or (
                        move.location_id.usage == 'inventory' and
                        move.location_dest_id.type_stock_loc == 'wip'):
                    ctx = self._context.copy()
                    ctx['force_company'] = move.company_id.id
                    journal_id, acc_src, acc_dest, acc_valuation =  \
                        quant_obj._get_accounting_data_for_valuation(move)
                    self.picking_account_move_generate(
                        move, acc_src, acc_dest, journal_id)

                if move.acc_move_id:
                    move_ids.append(move.acc_move_id.id)
            if move_ids:
                pick.am_ids = move_ids
