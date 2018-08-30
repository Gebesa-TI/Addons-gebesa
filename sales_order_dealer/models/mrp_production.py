# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'


    dealer_id = fields.Many2one('res.partner', string="Comerciante",)