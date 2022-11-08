# -*- coding: utf-8 -*-
{
    'name': 'Employee Request',
    "author": "Hashcode IT Solutions",
    'website': 'https://hashcodeit.com/',
    'version': '15.0.1.0.0',
    'support': 'info@hashcodeit.com',
    'category': 'Employee',
    'summary': 'Employee Certificate Request from portal',
    'description': """ """,
    'depends': ['base', 'odoo_custom_portal','mail', 'portal',],

    'data': [


    ],

    'assets': {
        'web.assets_qweb': [
        ],
        'web.assets_backend': [

            # 'hc_portal_document_request/static/src/js/Main.js',
            # 'hc_portal_document_request/static/src/js/CertificateRequests/CertificateRequests.js',



        ],
        'web.assets_frontend': [

        ],
        'odoo_custom_portal.assets_qweb': [

            'hc_portal_document_request/static/src/xml/certificate_request.xml',
            'hc_portal_document_request/static/src/xml/CertificateRequests.xml',
            'hc_portal_document_request/static/src/js/Downloads/CertificateDownloads.xml',

        ],




        'odoo_custom_portal.webclient': [


        #     'hc_portal_document_request/static/src/js/Main.js',

            # ('replace', 'odoo_custom_portal/static/src/js/MainPortal/MainPortal.js',
            #  'hc_portal_document_request/static/src/js/Main.js'),

                # ("remove", "odoo_custom_portal/static/src/js/MainPortal/MainPortal.js"),

            # 'hc_portal_document_request/static/src/js/Main.js',
            'hc_portal_document_request/static/src/js/CertificateRequests/CertificateRequests.js',
            'hc_portal_document_request/static/src/js/MainPortal/MainPortal.js',
            'hc_portal_document_request/static/src/js/Downloads/CertificateDownloads.js',

            #
        ],


    },

    "images": ["static/description/icon.png"],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
