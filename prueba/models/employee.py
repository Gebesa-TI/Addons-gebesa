# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    name_course = fields.Many2one('curso.prueba', string="Nombre del Cursos",)
