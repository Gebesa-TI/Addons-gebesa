# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type_id = fields.Many2one(
        'res.partner.type',
        string=_('Partner type'),
        ondelete='restrict'
    )


class ResPartnerType(models.Model):
    _name = 'res.partner.type'

    name = fields.Char(
        string=_('Name'),
    )
    code = fields.Char(
        string=_('Code'),
    )
