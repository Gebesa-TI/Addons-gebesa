# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Sale Date",
    "summary": "Add fields in invoice for requirements of sale data",
    "version": "9.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro Preciado>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "account",
    ],
    "data": [
        "views/account_invoice_view.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
