# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_cut_order'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_cut_order')
        obj_segment = self.env['mrp.segment']
        segments = obj_segment.browse(self._ids)
        docs = []
        for seg in segments:
            products = {}
            for seg_line in seg.line_ids:
                production = seg_line.mrp_production_id
                product = production.product_id
                if production.product_id.id in products.keys():
                    products[product.id]['product_qty'] += \
                        production.product_qty
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
                        if prod_line not in products[product.id][
                                'cut_line'].keys():
                            products[product.id]['cut_line'][prod_line] = []
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
                'name': seg.name,
                'folio': seg.folio,
                'products': products,
            })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }

        return report_obj.render(
            'mrp_segment.report_cut_order', docargs)
