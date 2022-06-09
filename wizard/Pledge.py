# -*- coding: utf-8 -*-
"""."""

from odoo import fields, models
import datetime
from odoo.exceptions import MissingError


class ChurchPledgeReport(models.TransientModel):
    """."""

    _name = 'ng_church.pledge_wizard'
    _description = "NG Church Pledge Wizard"

    pledge = fields.Many2one(
        'ng_church.pledge', string="Pledge", required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(
        string='End Date',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))

    def _report_exist(self, report):
        # check if incomming report is empty, if true return MissingError
        if len(report) <= 0:
            raise MissingError('Pledge record does not'
                               ' exist for selected date range.')

    def print_pledge_report(self, docids=None, data=None):
        """."""
        self.ensure_one()
        pledge = self.pledge
        report = self.env['ng_church.pledge_line'].search(
            [('pledge_id', '=', pledge.id)])
        self._report_exist(report)
        if self.date_from and self.date_to:
            pledge_line_from = report.filtered(
                lambda r: r.date >= self.date_from)
            pledge_line_to = pledge_line_from.filtered(
                lambda r: r.date <= self.date_to)
            self._report_exist(pledge_line_to)
            datas = {
                'pledge_lines': pledge_line_to.ids,
                'docids': pledge.id
            }
            return self.env.ref(
                'ng_church.ng_church_pledges_report').report_action(
                pledge, data=datas)
        else:
            raise MissingError('Record not found')
        # report = self.pledge.name.name
        # pledges = self.env['ng_church.pledge'].search([('name', '=', report)])
        # return self.env.ref(
        #     'ng_church.ng_church_pledges_report').report_action(
        #     pledges, data=data)
