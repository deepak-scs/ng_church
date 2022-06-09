# -*- coding: utf-8 -*-
"""Church donation report wizard."""
from odoo.addons.ng_church.wizard.helper import _report_range
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
    donation = fields.Many2one('ng_church.donation', required=True)

    def print_donation_report(self, docids=None, data=None):
        """."""
        church = [('church_id', '=', self.env.user.company_id.id),
                  ('id', '=', self.donation.id)]
        donation = self.donation.search(church).donation_line_ids
        donations = _report_range(donation, self.date_from, self.date_to)
        if len(donations) > 0:
            return self.env.ref(
                'ng_church.ng_church_donation_report').report_action(
                donations, data=data)
        raise MissingError('Record not found')
