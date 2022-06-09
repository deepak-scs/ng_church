# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class ChurchDonationLineAbstractModel(models.AbstractModel):
    """Church DonationLine Abstract Model."""

    _name = 'report.ng_church.church_donation_report'
    _description = "Report NG Church Church Donation Report"

    def donation_caculator(self, model):
        """donation_caculator."""
        return sum(donation.amount for donation in model)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.donation'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.offering',
            'docs': self.env['ng_church.donation_line'].browse(docids),
            'donation_caculator': self.donation_caculator
        }
