from openerp import models, fields, api


class AcountInvoice(models.Model):
	_name = 'account.invoice'
	_inherit ='account.invoice'

	dealer_id = fields.Many2one('res.partner', string="Comerciante")
    
class ResPartner(models.Model):
 	_name = 'res.partner'
 	_inherit = 'res.partner'
   		
   	carrera = fields.Text(
    		string='Carrera',
    		)