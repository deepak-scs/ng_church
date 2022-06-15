# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class ChurchOfferingLineAbstractModel(models.AbstractModel):
    """Church OfferingLine Abstract Model."""

    _name = 'report.ng_church.church_offering_report'
    _description = "Report NG Church Church Offering Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.program'].browse(
            data.get('docids'))
        offering_lines = self.env['ng_church.offering_line'].browse(
            data.get('offering_lines'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.program',
            'docs': docs,
            'offering_lines': offering_lines,
        }
