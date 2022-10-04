# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree, html
import odoo
from odoo import http
from odoo.addons.web.controllers import main
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.tools.misc import str2bool, xlsxwriter, file_open, file_path
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.tools import float_round

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'
db_monodb = http.db_monodb


class PortalHomePage(CustomerPortal):

    def _prepare_project_sharing_session_info(self):
        session_info = request.env['ir.http'].session_info()
        user_context = request.session.get_context() if request.session.uid else {}
        project_company = request.env['res.company'].sudo().search([
            ('id', '=', (request.env.context['allowed_company_ids'][0])), ], limit=1)
        session_info.update(
            user_companies={
                'current_company': project_company.id,
                'allowed_companies': {
                    project_company.id: {
                        'id': project_company.id,
                        'name': project_company.name,
                    },
                },
            },
            # FIXME: See if we prefer to give only the currency that the portal user just need to see the correct information in project sharing
            # currencies=request.env['ir.http'].get_currencies(),
        )
        return session_info

    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super(PortalHomePage, self).home(**kw)
        values = self._prepare_portal_layout_values()
        print('gotacha')
        # action_id = request.env.ref('odoo_custom_portal.HomePage2')
        # print(action_id.id)
        return request.render("odoo_custom_portal.web_frontend_layout_home",
                              {'session_info': self._prepare_project_sharing_session_info()}, )

    @http.route(['/my/my-profile'], type='http', auth="user", website=True)
    def my_profile(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("odoo_custom_portal.portal_my_profile", values)

    @http.route(['/odoo_custom_portal/dashboard_data'], type='json', auth="user", website=True)
    def my_profile(self, **kw):
        data = []
        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        attendances = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id)], limit=10)
        leave_balances_data = request.env['hr.leave.type'].sudo().get_days_all_request()
        leave_requests = request.env['hr.leave'].sudo().search([('employee_id', '=', employee_id)], order='id DESC',
                                                               limit=10)
        employee_data = {}
        leave_requests_data = []
        attendances_data = []

        if len(employee) == 1:
            employee_data = {
                'id': employee.id,
                'name': employee.name,
                'job_title': employee.job_title,
                'mobile_phone': employee.mobile_phone,
                'work_email': employee.work_email,
                'work_phone': employee.work_phone,
                'department_id': [employee.department_id.id,
                                  employee.department_id.name] if employee.department_id.id else False,
                'parent_id': [employee.parent_id.id, employee.parent_id.name] if employee.parent_id.id else False,
                'coach_id': [employee.coach_id.id, employee.coach_id.name] if employee.coach_id.id else False,
                'work_location_id': [employee.work_location_id.id,
                                     employee.work_location_id.name] if employee.work_location_id.id else False,
                'resource_calendar_id': [employee.resource_calendar_id.id,
                                         employee.resource_calendar_id.name] if employee.resource_calendar_id.id else False,
                'tz': employee.tz

            }
        for attendance in attendances:
            attendances_data.append({
                'id': attendance.id,
                'check_in': attendance.check_in,
                'check_out': attendance.check_out,
                'worked_hours': float_round(68.348787, precision_rounding=0.01)
            })

        for leave_request in leave_requests:
            print(dict(leave_request._fields['state'].selection)[leave_request.state])
            leave_requests_data.append({
                'id': leave_request.id,
                'holiday_status_id': [leave_request.holiday_status_id.id,
                                      leave_request.holiday_status_id.name] if leave_request.holiday_status_id.id else False,
                'date_from': leave_request.date_from,
                'date_to': leave_request.date_to,
                'duration_display': leave_request.duration_display,
                'state':dict(leave_request._fields['state'].selection)[leave_request.state]
            })

        return [{'employee_data': employee_data, 'attendances_data': attendances_data,
                 'leave_balances_data': leave_balances_data, 'leave_requests_data': leave_requests_data}]

    # @http.route(['/web/dataset/call_kw', '/web/dataset/call_kw/<path:path>'], type='json', auth="user")
    # def call_kw(self, model, method, args, kwargs, path=None):
    #     return self._call_kw(model, method, args, kwargs)
