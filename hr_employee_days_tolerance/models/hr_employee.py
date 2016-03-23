# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    tolerance_days = fields.Integer(string=_(u'Tolerance Days'))
