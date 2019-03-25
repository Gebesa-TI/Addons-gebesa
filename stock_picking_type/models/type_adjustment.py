# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class TypeAdjustment(models.Model):
    _name = 'type.adjustment'
    _description = 'Type of adjustment'
    _order = 'consecutive asc'
    _rec_name = 'description'

    @api.model
    def _default_consecutive(self):
        last_id = 0
        get_count = self.search_count([(1, '=', 1)])
        if get_count:
            last_id = get_count + 1
        else:
            last_id = 1
        consecutive = str(last_id).rjust(5, '0')
        return consecutive

    consecutive = fields.Char(
        string=_(u'Key'), size=5,
        default=_default_consecutive,
        help=_(u'Key type of adjustment'),
    )

    description = fields.Char(
        string=_(u'Description'), size=150,
        help=_(u'Description type of adjustment')
    )

    type_adjustment = fields.Selection(
        [('input', _(u'Input')),
         ('output', _(u'Output'))],
        string=_(u"Type of adjustment"),
    )

    type_calculation = fields.Selection(
        [('none', _(u'None')),
         ('extra_outputs', _(u'Extra outputs')),
         ('net_changes', _(u'Net changes')),
         ('extra_inputs', _(u'Extra inputs'))],
        string=_(u"Type of calculation"),
    )

    account_id = fields.Many2one(
        'account.account', string=_(u'Account'),
    )
    company_id = fields.Many2one(
        'res.company', string=_(u'Company'),
    )
    active = fields.Boolean(
        default=True,
        help="Set active to false to hide the tax without removing it.")

    _sql_constraints = [
        ('_check_consecutive_uniq', 'unique (consecutive)',
         _(u'This field must be unique!'))
    ]
