# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order',
                              ondelete='set null',
                              string=_(u'Sale Order'),
                              select=True)
