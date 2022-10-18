# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Custom Portal',
    'version': '1.0',
    'sequence': 1,
    'category': '',
    'website': '',
    'summary': '',
    'description': """  """,
    'depends': [
        'base',
        'mail', 'portal', 'project', 'hr_timesheet',
    ],
    'data': [
        'views/header_template.xml',

    ],

    'demo': [],

    'installable': True,
    'application': True,
    'assets': {
        'web.assets_qweb': [
        ],
        'web.assets_backend': [

        ],
        'web.assets_frontend': [

        ],
        'odoo_custom_portal.assets_qweb': [
            ('include', 'web.assets_qweb'),
            'odoo_custom_portal/static/src/js/StartPortal/PortalClient.xml',
            'odoo_custom_portal/static/src/js/MainPortal/MainPortal.xml',
            'odoo_custom_portal/static/src/js/DashBoard/DashBoard.xml',
            'odoo_custom_portal/static/src/js/Alerts/Alerts.xml',
            'odoo_custom_portal/static/src/js/Downloads/Downloads.xml',
            'odoo_custom_portal/static/src/js/MyProfile/MyProfile.xml',
            'odoo_custom_portal/static/src/js/MyShifts/MyShifts.xml',
            'odoo_custom_portal/static/src/js/Newsletter/Newsletter.xml',
            'odoo_custom_portal/static/src/js/Requests/Requests.xml',
        ],
        'odoo_custom_portal.webclient': [
            ('include', 'web.assets_backend'),
            # ('remove', 'web/static/src/webclient/menus/*.js'),

            # Remove Longpolling bus and packages needed this bus
            ('remove', 'bus/static/src/js/services/assets_watchdog_service.js'),
            ('remove', 'mail/static/src/services/messaging/messaging.js'),

            ('remove', 'mail/static/src/components/dialog_manager/dialog_manager.js'),
            ('remove', 'mail/static/src/services/dialog_service/dialog_service.js'),
            ('remove', 'mail/static/src/components/chat_window_manager/chat_window_manager.js'),
            ('remove', 'mail/static/src/services/chat_window_service/chat_window_service.js'),
            'odoo_custom_portal/static/src/fonts/fonts.scss',
            'odoo_custom_portal/static/src/js/MainPortal/MainPortal.css',
            'odoo_custom_portal/static/src/js/DashBoard/DashBoard.scss',
            'odoo_custom_portal/static/src/js/Alerts/Alerts.css',
            'odoo_custom_portal/static/src/js/Downloads/Downloads.scss',
            'odoo_custom_portal/static/src/js/MyProfile/MyProfile.scss',
            'odoo_custom_portal/static/src/js/MyShifts/MyShifts.scss',
            'odoo_custom_portal/static/src/js/Newsletter/Newsletter.scss',
            'odoo_custom_portal/static/src/js/Requests/Requests.scss',
            'web/static/src/legacy/js/public/public_widget.js',
            # 'portal/static/src/js/portal_chatter.js',
            # 'portal/static/src/js/portal_composer.js',
            # 'project/static/src/project_sharing/search/favorite_menu/custom_favorite_item.xml',
            # 'project/static/src/project_sharing/**/*.js',
            # 'project/static/src/scss/project_sharing/*',
            'odoo_custom_portal/static/src/js/StartPortal/startWebClient.js',
            'odoo_custom_portal/static/src/js/StartPortal/PortalClient.js',
            'odoo_custom_portal/static/src/js/MainPortal/MainPortal.js',
            'odoo_custom_portal/static/src/js/DashBoard/DashBoard.js',
            'odoo_custom_portal/static/src/js/Alerts/Alerts.js',
            'odoo_custom_portal/static/src/js/Downloads/Downloads.js',
            'odoo_custom_portal/static/src/js/MyProfile/MyProfile.js',
            'odoo_custom_portal/static/src/js/MyShifts/MyShifts.js',
            'odoo_custom_portal/static/src/js/Newsletter/Newsletter.js',
            'odoo_custom_portal/static/src/js/Requests/Requests.js',
            # 'odoo_custom_portal/static/src/js/home.js',

            'web/static/src/start.js',
            'web/static/src/legacy/legacy_setup.js',

        ],
        'odoo_custom_portal.assets_qweb_shift_view': [
            ('include', 'web.assets_qweb'),
            'odoo_custom_portal/static/src/js/StartShiftView/PortalShiftView.xml',
            'odoo_custom_portal/static/src/js/StartShiftView/ControlPanelShiftView.xml',

        ],
        'odoo_custom_portal.shift_view_webclient': [
            ('include', 'web.assets_backend'),
            # ('remove', 'web/static/src/webclient/menus/*.js'),

            # Remove Longpolling bus and packages needed this bus
            ('remove', 'bus/static/src/js/services/assets_watchdog_service.js'),
            ('remove', 'mail/static/src/services/messaging/messaging.js'),

            ('remove', 'mail/static/src/components/dialog_manager/dialog_manager.js'),
            ('remove', 'mail/static/src/services/dialog_service/dialog_service.js'),
            ('remove', 'mail/static/src/components/chat_window_manager/chat_window_manager.js'),
            ('remove', 'mail/static/src/services/chat_window_service/chat_window_service.js'),
            'odoo_custom_portal/static/src/fonts/fonts.scss',
            'odoo_custom_portal/static/src/js/StartShiftView/startWebClient.js',
            'odoo_custom_portal/static/src/js/StartShiftView/PortalShiftView.js',
            'odoo_custom_portal/static/src/js/StartShiftView/ShiftViewControlPanel.js',
            'odoo_custom_portal/static/src/js/StartShiftView/ControlPanelShiftView.js',

            'web/static/src/start.js',
            'web/static/src/legacy/legacy_setup.js',

        ],


    },
    'license': 'LGPL-3',
}
