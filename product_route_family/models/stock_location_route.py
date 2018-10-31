# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    product_family_id = fields.Many2one(
        'product.family',
        string=_("Preferred for family"),
    )
