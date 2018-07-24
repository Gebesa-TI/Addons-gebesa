# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_cut_order_production_consolidado'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_cut_order_production_consolidado')
        obj_production = self.env['mrp.production']
        mrp_production = obj_production.browse(self._ids)
        if len(mrp_production.mapped('product_id')) != 1:
            raise ValidationError(_("Todas las ordernes de fabricacion tienen \
                que tener el mismo producto"))
        docs = []
        products = {}
        name = ''
        for production in mrp_production:
            name += production.name + ', '
            product = production.product_id
            if product.id in products.keys():
                products[product.id][
                    'product_qty'] += production.product_qty
            else:
                products[product.id] = {
                    'product_name': product.name,
                    'product_qty': production.product_qty,
                    'product_code': product.default_code,
                    'cut_line': {}
                }
            bom_lines = production.bom_id.bom_line_ids
            for bom_line in bom_lines:
                for bom_line_det in bom_line.bom_line_detail_ids:
                    prod_line = bom_line_det.production_line_id.description
                    if prod_line not in products[
                            product.id]['cut_line'].keys():
                        products[product.id]['cut_line'][
                            prod_line] = []
                    add = True
                    for cut in products[product.id]['cut_line'][prod_line]:
                        if cut['name'] == bom_line_det.name and \
                                cut['caliber'] == bom_line_det.caliber_id and \
                                cut['width'] == bom_line_det.width_cut and \
                                cut['long'] == bom_line_det.long_cut:
                            cut['qty'] += bom_line_det.quantity * \
                                production.product_qty
                            add = False
                    if add:
                        products[product.id]['cut_line'][prod_line].append({
                            'name': bom_line_det.name,
                            'caliber': bom_line_det.caliber_id,
                            'width': bom_line_det.width_cut,
                            'long': bom_line_det.long_cut,
                            'qty': bom_line_det.quantity * production.product_qty
                        })

            for product in products.keys():
                for prod_line in products[product]['cut_line'].keys():
                    products[product]['cut_line'][prod_line] = sorted(
                        products[product]['cut_line'][prod_line],
                        key=lambda cut: cut['long'])
                    products[product]['cut_line'][prod_line] = sorted(
                        products[product]['cut_line'][prod_line],
                        key=lambda cut: cut['width'])
                    products[product]['cut_line'][prod_line] = sorted(
                        products[product]['cut_line'][prod_line],
                        key=lambda cut: cut['caliber'].key_caliber)
                    products[product]['cut_line'][prod_line] = sorted(
                        products[product]['cut_line'][prod_line],
                        key=lambda cut: cut['name'])

        docs.append({
            'name': name,
            'folio': None,
            'products': products,
        })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }

        return report_obj.render(
            'mrp_segment.report_cut_order_production_consolidado',
            docargs)
