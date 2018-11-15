# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)

class MrpBomLineMassiveReplacement(models.TransientModel):
    _name = "mrp.bom.line.massive.replacement"

    product_id = fields.Many2one(
        'product.product',
        string='Product origin',
    )
    new_product_id = fields.Many2one(
        'product.product',
        string='New product',
    )
    limit = fields.Integer(
        string='Limite',
    )

    @api.multi
    def process(self):
        _logger.warning(
            _('GEB - Entrando al metodo'))
        bom_line_obj = self.env['mrp.bom.line']
        for replacement in self:
            _logger.warning(
                _('GEB - limite %s') % str(replacement.limit))
            if replacement.limit > 0:
                bom_line = bom_line_obj.search(
                    [('product_id', '=', replacement.product_id.id)],
                    limit=replacement.limit)
            else:
                bom_line = bom_line_obj.search(
                    [('product_id', '=', replacement.product_id.id)])
            done_ids = []
            _logger.warning(
                _('GEB - num reemp %s') % str(len(bom_line)))
            for line in bom_line:
                line.product_id = replacement.new_product_id.id
                if line.bom_id.id in done_ids:
                    continue
                _logger.warning(
                    _('GEB - ACTUAL %s') % line.bom_id.product_id.name)
                done_ids.append(line.bom_id.id)

            _logger.warning(
                _('GEB - Entrando revaluar'))

            # Revaluacion
            for bom in done_ids:
                self.env['mrp.bom'].browse(bom).action_reval()

            _logger.warning(
                _('GEB - termina de revaluar'))
