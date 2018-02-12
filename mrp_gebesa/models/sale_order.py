# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    city_id = fields.Many2one(
        'res.country.state.city',
        string=_('City'),
        readonly=True,
        related='partner_shipping_id.city_id'
    )

    state_id = fields.Many2one(
        'res.country.state',
        string=_('State'),
        readonly=True,
        related='partner_shipping_id.state_id'
    )

    country_id = fields.Many2one(
        'res.country',
        string=_('Country'),
        readonly=True,
        related='partner_shipping_id.country_id'
    )
