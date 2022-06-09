# -*- coding: utf-8 -*-
"""."""

from odoo import api, models

class ChurchAttendanceLineAbstractModel(models.AbstractModel):
    """PledgesReport."""

    _name = 'report.ng_church.church_attendance_report'
    _description = "Report NG Church Church Attendance Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.program'].browse(
            data.get('docids'))
        attendance_lines = self.env['ng_church.attendance_line'].browse(
            data.get('attendance_lines'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.program',
            'docs': docs,
            'attendance_lines': attendance_lines,
        }
