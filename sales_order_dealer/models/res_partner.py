# -*- coding: utf-8 -*-
# Copyright 2019, Samuel Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    requires_dealer = fields.Boolean(
        string=_('Requires dealer'),
    )
