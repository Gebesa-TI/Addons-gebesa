from openerp import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "openacademy"
    _rec_name ='name'

    name = fields.Char(
    		string='Titulo',
    		required=True,
    		)

    description = fields.Text(
    		string='description',
    		)



