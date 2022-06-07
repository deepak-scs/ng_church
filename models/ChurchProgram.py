# *-* coding:utf-8 -*-
"""."""
from odoo import api, fields, models
from .helper import parish
from odoo.exceptions import ValidationError


class ChurchProgram(models.Model):
    """ChurchService."""
    _name = 'ng_church.program'
    _description = "NG Church Program"

    name = fields.Char('Name', required=True)
    days = fields.Selection([
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], string='Day', default='Monday', required=True)
    start = fields.Float(string='Start Time')
    start_meridiem = fields.Selection([
        ('AM', 'AM'),
        ('PM', 'PM')
    ], string='')
    end = fields.Float(string='End Time')
    end_meridiem = fields.Selection([
        ('AM', 'AM'),
        ('PM', 'PM')
    ], string='')
    parish_id = fields.Many2one('res.company', string='Parish', default=parish)

    @api.constrains('start', 'end')
    def _check_start_end_time(self):
        for rec in self:
            if rec.start > 12 or rec.end > 12:
                raise ValidationError('Start time or End time less than 12')
            if rec.end < rec.start:
                if rec.start_meridiem == rec.end_meridiem:
                    raise ValidationError(
                        'Start time is not greater than end time')
            if rec.end == rec.start:
                if rec.start_meridiem == rec.end_meridiem:
                    raise ValidationError(
                        'Start time and end time should be different!.')

    @api.constrains('start_meridiem', 'end_meridiem')
    def _check_start_meridiem_end_meridiem(self):
        for rec in self:
            if rec.end < rec.start:
                if rec.start_meridiem == rec.end_meridiem:
                    raise ValidationError(
                        'Start time is not greater than end time')
            if rec.end == rec.start:
                if rec.start_meridiem == rec.end_meridiem:
                    raise ValidationError(
                        'Start time and end time should be different!.')
