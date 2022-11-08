# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree, html
import odoo
import io
import re
from odoo import http, fields
import operator
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
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.tools.translate import _

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'
db_monodb = http.db_monodb


class PortalHomePage(CustomerPortal):
    @http.route(['/hc_portal_document_request/certificate_request'], type='json', auth="user", website=True)
    def my_certificate(self, ):
        data = []
        employee_id = request.env.user.employee_id.id
        print("sadjasdj", employee_id)
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        print("sjndjsand", employee)

        employee_data = {}
        if len(employee) == 1:
            print(employee.gender)
            employee_data = {
                'id': employee.id,
                'countries_ids': [[country.id, country.display_name] for country in
                                  request.env['certificate.type'].sudo().search([])],

            }

        print("sdasjndjasn rr", employee_data)
        return [{'employee_data': employee_data, }]

    @http.route(['/hc_portal_document_request/certificate_request/save-data'], type='json', auth="user", website=True)
    def my_certificate_save_data(self, saving_data):
        data = []
        print("uuuuuuuuuuuuu", saving_data, fields.Datetime.now(), request.env['certificate.type'].sudo().browse(saving_data.get('certificate_type')))
        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)

        if len(saving_data) > 0:
            if len(employee) == 1:
                employee_data = {
                    'employee_id': employee.id,
                    'certificate_type_id': request.env['certificate.type'].sudo().browse(saving_data.get('certificate_type')).id if saving_data.get('certificate_type') else False,
                    'requested_date': fields.Datetime.now(),
                    'address': saving_data.get('addressee'),
                    'travel_dest': saving_data.get('travel'),
                    'issued_to': saving_data.get('issued_to'),

                }

                print("employee_data ccccc", employee_data)
                request.env['certificate.request'].sudo().create(employee_data)
                print(employee_data)



        return True

    @http.route(['/hc_portal_document_request/certificate_data'], type='json', auth="user", website=True)
    def download_certificate(self, page_number, items_per_page):

        print("sssssssssss111111111s")

        employee_id = request.env.user.employee_id.id
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        # ('employee_id', '=', employee_id)
        payslips_count = request.env['certificate.request'].sudo().search_count([('employee_id', '=', employee_id)])
        payslips = request.env['certificate.request'].sudo().search([('employee_id', '=', employee_id)], limit=items_per_page,
                                                           order='id DESC', offset=(page_number - 1) * items_per_page)
        payslips_data = []
        employee_data = {}

        def payslip_state_colors(state):
            print("Sdasdkm", state)
            if state == 'draft':
                return {'background': '#8bd0db'}
            elif state == 'under_review':
                return {'background': '#fed47e'}
            elif state == 'send_for_approval':
                return {'background': '#92d2a1'}
            elif state == 'approved':
                return {'background': '#92d2a1'}
            elif state == 'canceled':
                return {'background': '#e8e8e8'}



        for payslip in payslips:
            # print(dict(leave_request._fields['state'].selection)[leave_request.state])
            payslips_data.append({
                'id': payslip.id,
                'is_selected': False,
                'number': payslip.name,
                'struct_id': [payslip.certificate_type_id.id,
                              payslip.certificate_type_id.name] if payslip.certificate_type_id.id else False,
                'requested_date': payslip.requested_date,
                'approved_date': payslip.requested_date,
                'destination': payslip.travel_dest,
                'issued_to': payslip.issued_to,
                'state': dict(payslip._fields['state'].selection)[payslip.state],
                'state_colors': payslip_state_colors(payslip.state)

            })

        print("sssssss  rrrr sssss", {'payslips_data': payslips_data, 'payslips_count': payslips_count, 'employee_data': employee_data, })
        return [{'payslips_data': payslips_data, 'payslips_count': payslips_count, 'employee_data': employee_data, }]

    @route(["/my/certificate/pdf/download"], type='http', auth="user", website=True)
    def get_certificate_report_print(self, list_ids='', **post):
        print("ASdasdasd", list_ids)
        if not list_ids or re.search("[^0-9|,]", list_ids):
            return request.not_found()

        ids = [int(s) for s in list_ids.split(',')]
        payslips = request.env['certificate.request'].sudo().browse(ids)

        pdf_writer = PdfFileWriter()

        for payslip in payslips:
            if payslip.state != 'approved':
                raise UserError("Please select Approved Only!....")
            report = request.env.ref('hc_certificate.action_report_certificate')
            # if not payslip.struct_id or not payslip.struct_id.report_id:
            #     report = request.env.ref('hr_payroll.action_report_payslip', False)
            # else:
            #     report = payslip.struct_id.report_id
            report = report.with_context(lang=payslip.employee_id.sudo().address_home_id.lang)
            pdf_content, _ = report.with_user(SUPERUSER_ID)._render_qweb_pdf(payslip.id,
                                                                             data={'company_id': request.env.user.company_id})
            reader = PdfFileReader(io.BytesIO(pdf_content), strict=False, overwriteWarnings=False)

            for page in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(page))

        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()

        # if len(payslips) == 1 and payslips.struct_id.report_id.print_report_name:
        #     report_name = safe_eval(payslips.struct_id.report_id.print_report_name, {'object': payslips})
        # else:
        report_name = request.env.ref('hc_certificate.action_report_certificate').name

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(merged_pdf)),
            ('Content-Disposition', content_disposition(report_name + '.pdf'))
        ]

        return request.make_response(merged_pdf, headers=pdfhttpheaders)