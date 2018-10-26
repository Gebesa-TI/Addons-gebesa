# -*- coding: utf-8 -*-
# © 2017 Aldo Nerio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Validate",
    "summary": "Stock Picking Validate",
    "version": "9.0.1.0.0",
    "category": "Personalized",
    "website": "https://odoo-community.org/",
    "author": "<Esther Cisneros>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_picking.xml",
        "security/security.xml",

    ],
    "demo": [
    ],
    "qweb": [
    ]
}
