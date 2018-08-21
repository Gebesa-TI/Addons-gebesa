# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OpenAcademy",
    "summary": "OpenAcademy",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Esther cisneros, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",

    ],
    "data": [
        'security/security.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'reports/reports.xml',

    ],
    "demo": [

    ],
    "qweb": [

    ]
}

