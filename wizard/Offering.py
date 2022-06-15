# -*- coding: utf-8 -*-
"""Church offering report wizard."""

import datetime
from odoo import fields, models
from odoo.exceptions import MissingError, UserError


class OfferingReportWizard(models.TransientModel):
    """."""

    _name = 'ng_church.offering_wizard'
    _description = "NG Church Offering Wizard"

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(
        string='Date to',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))
    service_id = fields.Many2one(
        'ng_church.program', required=True, string='Church Service')
    section_id = fields.Many2one(
        'church.sections', string="Church Section", required=True)

    def print_offering_report(self, docids=None, data=None):
        """."""
        offering_rec = self.env['ng_church.offering'].search([
            ('service_id', '=', self.service_id.id),
            ('section_id', '=', self.section_id.id),
        ])
        offering_line_rec = self.env['ng_church.offering_line'].search([
            ('offering_id', 'in', offering_rec.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        if offering_line_rec:
            datas = {
                'offering_lines': offering_line_rec.ids,
                'docids': self.service_id.id
            }
            return self.env.ref(
                'ng_church.ng_church_offering_report').report_action(
                self.service_id, data=datas)
        else:
            raise MissingError('Data not found!')
