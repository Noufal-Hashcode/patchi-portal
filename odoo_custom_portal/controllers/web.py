# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree, html
import odoo
import io
import re
from odoo import http
from odoo.addons.web.controllers import main
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.tools.misc import str2bool, xlsxwriter, file_open, file_path
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.tools import float_round
from odoo import exceptions, SUPERUSER_ID
from odoo.tools import consteq
from PyPDF2 import PdfFileReader, PdfFileWriter
from odoo.tools.safe_eval import safe_eval

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

    @http.route(['/my/shift-gannt-view'], type='http', auth="user", website=True)
    def shift_view(self, **kw):
        values = self._prepare_portal_layout_values()
        print('gotacha')
        # action_id = request.env.ref('odoo_custom_portal.HomePage2')
        # print(action_id.id)
        return request.render("odoo_custom_portal.odoo_custom_portal_shift",
                              {'session_info': self._prepare_project_sharing_session_info()}, )



    # @http.route(['/my/my-profile'], type='http', auth="user", website=True)
    # def my_profile(self, **kw):
    #     values = self._prepare_portal_layout_values()
    #     return request.render("odoo_custom_portal.portal_my_profile", values)

    @http.route(['/odoo_custom_portal/dashboard_data'], type='json', auth="user", website=True)
    def dash_board(self, page_number, items_per_page):
        data = []
        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        attendances = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id)],
                                                                 limit=items_per_page,
                                                                 order='id DESC',
                                                                 offset=(page_number - 1) * items_per_page)
        attendances_count = request.env['hr.attendance'].sudo().search_count([('employee_id', '=', employee_id)])
        leave_balances_data = request.env['hr.leave.type'].sudo().get_days_all_request()
        leave_requests = request.env['hr.leave'].sudo().search([('employee_id', '=', employee_id)],
                                                               limit=items_per_page,
                                                               order='id DESC',
                                                               offset=(page_number - 1) * items_per_page)
        leave_requests_count = request.env['hr.leave'].sudo().search_count([('employee_id', '=', employee_id)])
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
                'leave_manager_id': [employee.leave_manager_id.id,
                                     employee.leave_manager_id.name] if employee.leave_manager_id.id else False,
                'expense_manager_id': [employee.expense_manager_id.id,
                                       employee.expense_manager_id.name] if employee.expense_manager_id.id else False,
                'timesheet_manager_id': [employee.timesheet_manager_id.id,
                                         employee.timesheet_manager_id.name] if employee.timesheet_manager_id.id else False,
                'work_location_id': [employee.work_location_id.id,
                                     employee.work_location_id.name] if employee.work_location_id.id else False,
                'private_email': employee.private_email,
                'phone': employee.phone,
                'children': employee.children,
                'gender': employee.gender,
                'marital': dict(employee._fields['marital'].selection)[employee.marital],
                'emergency_contact': employee.emergency_contact,
                'emergency_phone': employee.emergency_phone,
                'birthday': employee.birthday,
                'resource_calendar_id': [employee.resource_calendar_id.id,
                                         employee.resource_calendar_id.name] if employee.resource_calendar_id.id else False,
                'tz': employee.tz,
                'countries_ids': [[country.id, country.display_name] for country in
                                  request.env['res.country'].sudo().search([])],
                'state_ids': [{state.id, state.display_name} for state in
                              request.env['res.country.state'].sudo().search([])]

            }
            print([{country.id, country.display_name} for country in
                   request.env['res.country'].sudo().search([])])
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
                'state': dict(leave_request._fields['state'].selection)[leave_request.state]
            })

        return [{'employee_data': employee_data, 'attendances_data': attendances_data,
                 'attendances_count': attendances_count,
                 'leave_balances_data': leave_balances_data, 'leave_requests_data': leave_requests_data,
                 'leave_requests_count': leave_requests_count}]

    @http.route(['/odoo_custom_portal/my-profile'], type='json', auth="user", website=True)
    def my_profile(self, ):
        data = []
        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)

        employee_data = {}
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
                'leave_manager_id': [employee.leave_manager_id.id,
                                     employee.leave_manager_id.name] if employee.leave_manager_id.id else False,
                'expense_manager_id': [employee.expense_manager_id.id,
                                       employee.expense_manager_id.name] if employee.expense_manager_id.id else False,
                'timesheet_manager_id': [employee.timesheet_manager_id.id,
                                         employee.timesheet_manager_id.name] if employee.timesheet_manager_id.id else False,
                'work_location_id': [employee.work_location_id.id,
                                     employee.work_location_id.name] if employee.work_location_id.id else False,
                'private_email': employee.private_email,
                'phone': employee.phone,
                'children': employee.children,
                'gender': employee.gender,
                'marital': [employee.marital, dict(employee._fields['marital'].selection)[employee.marital]],
                'marital_statuses': dict(employee._fields['marital'].selection),
                'emergency_contact': employee.emergency_contact,
                'emergency_phone': employee.emergency_phone,
                'birthday': employee.birthday,
                'resource_calendar_id': [employee.resource_calendar_id.id,
                                         employee.resource_calendar_id.name] if employee.resource_calendar_id else False,
                'tz': employee.tz,
                'countries_ids': [[country.id, country.display_name] for country in
                                  request.env['res.country'].sudo().search([])],
                'state_ids': [[state.id, state.display_name] for state in
                              request.env['res.country.state'].sudo().search(
                                  [('country_id', '=', employee.address_home_id.country_id.id)])],
                'address_home_id': {'street': employee.address_home_id.street,
                                    'street2': employee.address_home_id.street2,
                                    'city': employee.address_home_id.city,
                                    'state_id': [employee.address_home_id.state_id.id,
                                                 employee.address_home_id.state_id.name] if employee.address_home_id.state_id else False,
                                    'zip': employee.address_home_id.zip,
                                    'country_id': [employee.address_home_id.country_id.id,
                                                   employee.address_home_id.country_id.name] if employee.address_home_id.country_id else False,
                                    }

            }

        return [{'employee_data': employee_data, }]

    @http.route(['/odoo_custom_portal/my-profile/save-data'], type='json', auth="user", website=True)
    def my_profile_save_data(self, saving_data):
        data = []
        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        if len(saving_data) > 0:
            if len(employee) == 1:
                employee_data = {
                    'birthday': saving_data['birthday'],
                    # 'marital': saving_data['marital'],
                    'children': saving_data['children'],
                    'emergency_contact': saving_data['emergency_contact'],
                    'emergency_phone': saving_data['emergency_phone'],

                }
                employee.write(employee_data)

            print(saving_data['private_email'])
            address_id = employee.address_home_id.write({
                'email': saving_data['private_email'],
                'phone': saving_data['phone'],
                'street': saving_data['address_home_id']['street'],
                'street2': saving_data['address_home_id']['street2'],
                'city': saving_data['address_home_id']['city'],
                'state_id': saving_data['address_home_id']['state_id'],
                'country_id': saving_data['address_home_id']['country_id'],
                'zip': saving_data['address_home_id']['zip'],

            })

        return True

    @http.route(['/odoo_custom_portal/payslips_data'], type='json', auth="user", website=True)
    def download_payslips(self, page_number, items_per_page):

        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        # ('employee_id', '=', employee_id)
        payslips_count = request.env['hr.payslip'].sudo().search_count([])
        payslips = request.env['hr.payslip'].sudo().search([], limit=items_per_page,
                                                           order='id DESC', offset=(page_number - 1) * items_per_page)
        payslips_data = []
        employee_data = {}

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
                'tz': employee.tz,
                'contract_id': [employee.contract_id.id,
                                employee.contract_id.name] if employee.contract_id.id else False,
                'job_id': [employee.job_id.id,
                           employee.job_id.name] if employee.job_id.id else False,
                'employee_type': dict(employee._fields['employee_type'].selection)[employee.employee_type],
                'first_contract_date': employee.first_contract_date

            }

        for payslip in payslips:
            # print(dict(leave_request._fields['state'].selection)[leave_request.state])
            payslips_data.append({
                'id': payslip.id,
                'is_selected': False,
                'number': payslip.number,
                'struct_id': [payslip.struct_id.id,
                              payslip.struct_id.name] if payslip.struct_id.id else False,
                'date_from': payslip.date_from,
                'date_to': payslip.date_to,
                'net_wage': payslip.net_wage,
                'basic_wage': payslip.basic_wage,
                'state': dict(payslip._fields['state'].selection)[payslip.state]
            })

        return [{'payslips_data': payslips_data, 'payslips_count': payslips_count, 'employee_data': employee_data, }]

    def _stock_picking_check_access(self, slips_ids, access_token=None):
        pay_slips = request.env['hr.payslip'].browse([slips_ids])
        pay_slips_sudo = pay_slips.sudo()
        try:
            pay_slips.check_access_rights('read')
            pay_slips.check_access_rule('read')
        except exceptions.AccessError:
            if not access_token or not consteq(pay_slips_sudo.sale_id.access_token, access_token):
                raise
        return pay_slips_sudo

    @route(['/my/payslips/pdf/download'], type='http', auth="public", website=True)
    def portal_my_payslips_report(self, access_token=None, **kw):
        # """ Print delivery slip for customer, using either access rights or access token
        # to be sure customer has access """
        # try:
        #     pay_slips_sudo = self._stock_picking_check_access(ids, access_token=access_token)
        # except exceptions.AccessError:
        #     return request.redirect('/my')
        #
        # # print report as SUPERUSER, since it require access to product, taxes, payment term etc.. and portal does not have those access rights.
        # pdf = request.env.ref('stock.action_report_delivery').with_user(SUPERUSER_ID)._render_qweb_pdf([pay_slips_sudo.id])[0]
        # pdfhttpheaders = [
        #     ('Content-Type', 'application/pdf'),
        #     ('Content-Length', len(pdf)),
        # ]
        # return request.make_response(pdf, headers=pdfhttpheaders)
        pdf = request.env.ref('hr_payroll.action_report_payslip').with_user(SUPERUSER_ID)._render_qweb_pdf([5])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @route(["/my/payslips/pdf/download"], type='http', auth="public", website=True)
    def get_payroll_report_print(self, list_ids='', **post):
        if not list_ids or re.search("[^0-9|,]", list_ids):
            return request.not_found()

        ids = [int(s) for s in list_ids.split(',')]
        payslips = request.env['hr.payslip'].sudo().browse(ids)

        pdf_writer = PdfFileWriter()

        for payslip in payslips:
            if not payslip.struct_id or not payslip.struct_id.report_id:
                report = request.env.ref('hr_payroll.action_report_payslip', False)
            else:
                report = payslip.struct_id.report_id
            report = report.with_context(lang=payslip.employee_id.sudo().address_home_id.lang)
            pdf_content, _ = report.with_user(SUPERUSER_ID)._render_qweb_pdf(payslip.id,
                                                                             data={'company_id': payslip.company_id})
            reader = PdfFileReader(io.BytesIO(pdf_content), strict=False, overwriteWarnings=False)

            for page in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(page))

        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()

        if len(payslips) == 1 and payslips.struct_id.report_id.print_report_name:
            report_name = safe_eval(payslips.struct_id.report_id.print_report_name, {'object': payslips})
        else:
            report_name = "Payslips"

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(merged_pdf)),
            ('Content-Disposition', content_disposition(report_name + '.pdf'))
        ]

        return request.make_response(merged_pdf, headers=pdfhttpheaders)

    # @http.route(['/web/dataset/call_kw', '/web/dataset/call_kw/<path:path>'], type='json', auth="user")
    # def call_kw(self, model, method, args, kwargs, path=None):
    #     return self._call_kw(model, method, args, kwargs)
