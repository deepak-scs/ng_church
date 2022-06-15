# -*- coding: utf-8 -*-
"""Church donation report wizard."""
import datetime
from odoo import fields, models
from odoo.exceptions import MissingError


class DonationReportWizard(models.TransientModel):
    """."""

    _name = 'ng_church.donation_wizard'
    _description = "NG Church Donation Wizard"

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(
        string='Date to',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))
    project_id = fields.Many2one('project.project', required=True)

    def print_donation_report(self, docids=None, data=None):
        """."""
        donation_rec = self.env['ng_church.donation'].search([
            ('project_id', '=', self.project_id.id)
        ])
        donation_line_rec = self.env['ng_church.donation_line'].search([
            ('donation_id', 'in', donation_rec.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        if donation_line_rec:
            datas = {
                'donation_lines': donation_line_rec.ids,
                'docids': self.project_id.id
            }
            return self.env.ref(
                'ng_church.ng_church_donation_report').report_action(
                self.project_id.id, data=datas)
        else:
            raise MissingError('Data not found!')
