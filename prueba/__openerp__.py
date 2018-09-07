# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Prueba Cursos",
    "summary": "Prueba Cursos",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Esther Cisneros, Odoo Community Association (OCA)",
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

    ],
    "data": [
        "security/security.xml",
        "views/curso_prueba.xml",
        "views/employee.xml",
        "wizards/status_course_wizard.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ]
}
