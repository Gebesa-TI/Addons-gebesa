# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models,_, api

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'


    dealer_id = fields.Many2one('res.partner', 
        string="Comerciante",
        )
