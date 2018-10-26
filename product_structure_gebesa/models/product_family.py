# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductFamily(models.Model):
    _name = 'product.family'
    _description = 'product.family'
    _order = "name asc"

    name = fields.Char(
        string=_('Name'),
        size=120,
        required=True,
        help=_('Family name product'),
    )

    active = fields.Boolean(
        string=_('Active'),
        default=True
    )

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_('Warehouse'),
    )

    parent_id = fields.Many2one(
        'product.family',
        string=_('Padre'),
    )

    analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_('Analítica'),
    )
