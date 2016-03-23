# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order - Add State",
    "summary": "Add a new state (Closed) in sale order",
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
        "sale",
    ],
    "data": [
        "views/sale_view.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
