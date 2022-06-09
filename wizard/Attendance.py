# -*- coding: utf-8 -*-
"""."""

from odoo import fields, models
from odoo.exceptions import MissingError
import datetime


class ChurchAttendanceLine(models.TransientModel):
    """."""

    _name = 'ng_church.attendance_wizard'
    _description = "NG Church Attendance Wizard"

    program_id = fields.Many2one(
        'ng_church.program', string="Service", required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(
        string='End Date',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))

    def print_attendance_report(self, docids=None, data=None):
        """."""
        self.ensure_one()
        attendance_rec = self.env['ng_church.attendance'].search([
            ('program_id', '=', self.program_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        if attendance_rec:
            datas = {
                'attendance_lines': [
                    line for line in attendance_rec.attendance_line_ids.ids],
                'docids': self.program_id.id
            }
            return self.env.ref(
                'ng_church.ng_church_attendance_line_report').report_action(
                self.program_id, data=datas)
        else:
            raise MissingError('Data not found!')
