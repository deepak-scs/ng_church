# -*- coding: utf-8 -*-
"""."""

from odoo import api, fields, models


class PledgesReport(models.AbstractModel):
    """PledgesReport."""

    _name = 'report.ng_church.church_pledges_report'
    _description = "Report NG Church Church Pledges Report"

    def reports_presenter(self, model):
        """Mutate the state of the original report(s)."""
        return model

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.pledge'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.pledge',
            'docs': self.env['ng_church.pledge'].browse(docids),
        }


class ChurchPledgeReport(models.TransientModel):
    """."""

    _name = 'ng_church.pledge_wizard'
    _description = "NG Church Pledge Wizard"

    pledge = fields.Many2one('ng_church.pledge', string="Pledge",
                             required=True)

    def print_pledge_report(self, docids=None, data=None):
        """."""
        report = self.pledge.name.name
        pledges = self.env['ng_church.pledge'].search([('name', '=', report)])
        return self.env.ref(
            'ng_church.ng_church_pledges_report').report_action(
            pledges, data=data)
