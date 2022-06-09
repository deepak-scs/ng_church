# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class ChurchOfferingLineAbstractModel(models.AbstractModel):
    """Church OfferingLine Abstract Model."""

    _name = 'report.ng_church.church_offering_report'
    _description = "Report NG Church Church Offering Report"

    def offering_caculator(self, model):
        """offering_caculator."""
        return sum(offering.amount for offering in model)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.offering'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.offering',
            'docs': self.env['ng_church.offering_line'].browse(docids),
            'offering_caculator': self.offering_caculator
        }
