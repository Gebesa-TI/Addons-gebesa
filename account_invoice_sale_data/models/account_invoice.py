# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _
from openerp.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    total_net_sale = fields.Float(
        string=_(u'Total net sale'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_freight = fields.Float(
        string=_(u'Freight percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_freight = fields.Float(
        string=_(u'Total Freight'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_installation = fields.Float(
        string=_(u'Installation percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_installation = fields.Float(
        string=_(u'Total installation'),
        digits_compute=dp.get_precision('Account'),
    )

    profit_margin = fields.Float(
        string=_(u'Profit margin'),
        digits_compute=dp.get_precision('Account'),
    )

    not_be_billed = fields.Boolean(
        string=_(u'Not be billed'),
    )

    manufacture = fields.Selection(
        [('special', _(u'Special')),
            ('line', _(u'Line')),
            ('replenishment', _(u'Replenishment')),
            ('semi_special', _(u'Semi special'))],
        string=_(u"Manufacture"),

    )

    executive = fields.Char(
        string=_(u'Executive'),
        size=100,
    )
