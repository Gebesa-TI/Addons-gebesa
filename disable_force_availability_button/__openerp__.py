# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Disable Force Availability Button",
    "summary": "Add privileges per group on the force-availability button.",
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
        "stock",
        "mrp",
        "system_administrator",
    ],
    "data": [
        "views/stock_picking_view.xml",
        "views/mrp_production_view.xml",
        "security/security.xml"
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
