# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class PledgesReport(models.AbstractModel):
    """PledgesReport."""

    _name = 'report.ng_church.church_pledges_report'
    _description = "Report NG Church Church Pledges Report"

    # def reports_presenter(self, model):
    #     """Mutate the state of the original report(s)."""
    #     return model

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.pledge'].browse(
            data.get('docids'))
        pledge_lines = self.env['ng_church.pledge_line'].browse(
            data.get('pledge_lines'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.pledge',
            'docs': docs,
            'pledge_lines': pledge_lines,
        }
