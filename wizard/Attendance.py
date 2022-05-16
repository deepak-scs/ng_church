# -*- coding: utf-8 -*-
"""."""

from odoo import api, fields, models
from odoo.exceptions import MissingError
import datetime


class ChurchAttendanceLineAbstractModel(models.AbstractModel):
    """PledgesReport."""

    _name = 'report.ng_church.church_attendance_report'
    _description = "Report NG Church Church Attendance Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.attendance'].browse(
            data.get('docids'))
        attendance_lines = self.env['ng_church.attendance_line'].browse(
            data.get('attendance_lines'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.attendance',
            'docs': docs,
            'attendance_lines': attendance_lines,
        }


class ChurchAttendanceLine(models.TransientModel):
    """."""

    _name = 'ng_church.attendance_wizard'
    _description = "NG Church Attendance Wizard"

    attendance = fields.Many2one(
        'ng_church.attendance', string="Service", required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(
        string='End Date',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))

    def _report_exist(self, report):
        # check if incomming report is empty, if true return MissingError
        if len(report) <= 0:
            raise MissingError('Attendance record does not'
                               ' exist for selected date range.')

    def print_attendance_report(self, docids=None, data=None):
        """."""
        self.ensure_one()
        attendance = self.attendance
        report = self.env['ng_church.attendance_line'].search(
            [('attendance_id', '=', attendance.id)])
        self._report_exist(report)
        if self.date_from and self.date_to:
            attendance_line_from = report.filtered(
                lambda r: r.date >= self.date_from)
            attendance_line_to = attendance_line_from.filtered(
                lambda r: r.date <= self.date_to)
            self._report_exist(attendance_line_to)
            datas = {
                'attendance_lines': attendance_line_to.ids,
                'docids': attendance.id
            }
            return self.env.ref(
                'ng_church.ng_church_attendance_line_report').report_action(
                attendance, data=datas)
        elif self.date_from:
            attendance_line_from = report.filtered(
                lambda r: r.date >= self.date_from)
            self._report_exist(attendance_line_from)
            datas = {
                'attendance_lines': attendance_line_from.ids,
                'docids': attendance.id
            }
            return self.env.ref(
                'ng_church.ng_church_attendance_line_report').report_action(
                attendance, data=datas)
        elif self.date_to:
            attendance_line_to = report.filtered(
                lambda r: r.date <= self.date_to)
            self._report_exist(attendance_line_to)
            datas = {
                'attendance_lines': attendance_line_to.ids,
                'docids': attendance.id
            }
            return self.env.ref(
                'ng_church.ng_church_attendance_line_report').report_action(
                attendance, data=datas)
        else:
            raise MissingError('Record not found')
