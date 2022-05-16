# -*- coding: utf-8 -*-
"""Church offering report wizard."""

import datetime
from odoo import api, fields, models
from odoo.exceptions import MissingError, UserError


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


class OfferingReportWizard(models.Model):
    """."""

    _name = 'ng_church.offering_wizard'
    _description = "NG Church Offering Wizard"

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(
        string='Date to',
        default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))
    offering = fields.Many2one('ng_church.program', required=True)

    def _report_range(self, model, after, before):
        if after > before:
            raise UserError('Date from is ahead of date to')
        if after and before:
            model = model.filtered(lambda r: r.date >= after)
            model = model.filtered(lambda r: r.date <= before)
            return model
        elif after:
            model = model.filtered(lambda r: r.date >= after)
            return model
        model = model.filtered(lambda r: r.date <= before)
        return model

    def print_offering_report(self, docids=None, data=None):
        """."""
        query = self.offering
        church = ('church_id', '=', self.env.user.company_id.id)
        services = self.env['ng_church.offering'].search([
            ('service_id', '=', query.id), church])
        offering_line = self.env['ng_church.offering_line']
        for offering in services:
            offering_line += offering_line.search(
                [('offering_id', '=', offering.id), church])
        offerings = self._report_range(
            offering_line, self.date_from, self.date_to)
        if len(offerings) > 0:
            return self.env.ref(
                'ng_church.ng_church_offering_report').report_action(
                offerings, data=data)
        raise MissingError('Record not found')
