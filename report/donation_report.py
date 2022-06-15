# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class ChurchDonationLineAbstractModel(models.AbstractModel):
    """Church DonationLine Abstract Model."""

    _name = 'report.ng_church.church_donation_report'
    _description = "Report NG Church Church Donation Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['project.project'].browse(
            data.get('docids'))
        donation_lines = self.env['ng_church.donation_line'].browse(
            data.get('donation_lines'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'project.project',
            'docs': docs,
            'donation_lines': donation_lines,
        }
