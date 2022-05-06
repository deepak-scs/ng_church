# -*- coding: utf-8 -*-
"""Church donation report wizard."""
from odoo.addons.ng_church.wizard.helper import _report_range
import datetime
from odoo import api, fields, models
from odoo.exceptions import MissingError


class ChurchDonationLineAbstractModel(models.AbstractModel):
    """Church DonationLine Abstract Model."""

    _name = 'report.ng_church.church_donation_report'
    _description = "Report NG Church Church Donation Report"

    def donation_caculator(self, model):
        """donation_caculator."""
        return sum(donation.amount for donation in model)

    # @api.model
    # def render_html(self, docids, data=None):
    #     """."""
    #     name = 'ng_church.church_donation_report'
    #     report_obj = self.env['report']
    #     report = report_obj._get_report_from_name(name)
    #     docargs = {
    #         'doc_ids': docids,
    #         'doc_model': report.model,
    #         'docs': self.env['ng_church.donation_line'].browse(docids),
    #         'donation_caculator': self.donation_caculator
    #     }
    #     return report_obj.render(name, docargs)
        
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.donation'].browse(docids)
        return {
        'doc_ids': docs.ids,
        'doc_model': 'ng_church.offering',
        'docs': self.env['ng_church.donation_line'].browse(docids),
        'donation_caculator': self.donation_caculator
        }

class DonationReportWizard(models.Model):
    """."""

    _name = 'ng_church.donation_wizard'
    _description = "NG Church Donation Wizard"

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(
        string='Date to',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))
    donation = fields.Many2one('ng_church.donation', required=True)

    def check_report(self):
        """."""
        church = [('church_id', '=', self.env.user.company_id.id),
                  ('id', '=', self.donation.id)]
        donation = self.donation.search(church).donation_line_ids
        donations = _report_range(donation, self.date_from, self.date_to)
        if len(donations) > 0:
            return self.env['report'].\
                get_action(donations, 'ng_church.church_donation_report')
        raise MissingError('Record not found')
