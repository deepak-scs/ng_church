# -*- coding: utf-8 -*-
"""."""

from odoo import api, models


class ChurchTitheLineAbstractModel(models.AbstractModel):
    """Church TitheLine Abstract Model."""

    _name = 'report.ng_church.church_tithe_report'
    _description = "Report NG Church Tithe"

    def tithe_caculator(self, model):
        """tithe_caculator."""
        return sum(tithe.amount for tithe in model)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['ng_church.tithe'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'ng_church.tithe',
            'docs': self.env['ng_church.tithe_lines'].browse(docids),
            'tithe_caculator': self.tithe_caculator
        }
