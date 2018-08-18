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
class Session(models.Model):
    _name = 'openacademy.session'


    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    