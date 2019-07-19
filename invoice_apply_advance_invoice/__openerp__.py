# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Apply Advance Invoice",
    "summary": "Apply advance invoice to an invoice",
    "version": "9.0.1.0.0",
    "category": "MPR",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "account",
        "account_invoice_prepayment",
        "account_invoice_sale_order_id",
        "account_analytic_everywhere",
        "account_invoice_line_analytic",
    ],
    "data": [
        "views/account_invoice_view.xml",
        "security/ir.mode.access.csv",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
