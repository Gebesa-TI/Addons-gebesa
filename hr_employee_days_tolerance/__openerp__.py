# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Days Tolerance Employee",
    "summary": "Assign tolerance days to create or modify movements.",
    "version": "9.0.1.0.0",
    "category": "",
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
        "base",
        "hr",
        "account",
    ],
    "data": [
        "views/hr_employee_view.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
