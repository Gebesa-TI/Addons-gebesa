# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Factoring Gebesa",
    "summary": "Add a new module for Customers and Suppliers for factoring",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro, Odoo Community Association (OCA)",
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
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/factoring_customer_view.xml",
        "views/factoring_supplier_view.xml",
        "views/factoring_secuence.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
