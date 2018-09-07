# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models

class StatusCourseWizard(models.TransientModel):
    _name = 'status.course.wizard'

    @api.multi
    def button_status_course_wizard(self):
    	status_obj = self.env['curso.prueba']
    	active_ids = self._context.get('active_ids', []) or []
    	status_var = status_obj.browse(active_ids)
    	for status in status_var:
    		status.status_course = 'finalized'
