# -*- coding: utf-8 -*-
{
    'name': 'Manager Database',
    'summary': "",
    'description': "Manager Database Name Of Users",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    'support': 'ipredictitsolutions@gmail.com',

    'category': 'Human Resources',
    'version': '16.0.1.0.0',
    'depends': ['hr', 'hr_attendance'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_user_view.xml'
    ],
    'assets': {

    },

    'currency': "EUR",
    'license': "OPL-1",

    'auto_install': False,
    'installable': True,
}
