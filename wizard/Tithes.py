# -*- coding: utf-8 -*-
"""Church tithe report wizard."""

import datetime
from odoo import api, fields, models
from odoo.exceptions import MissingError, UserError


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


class TitheReportWizard(models.Model):
    """."""

    _name = 'ng_church.tithe_wizard'
    _description = "NG Church Tithe Wizard"

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(
        string='Date to', default=lambda self: datetime.datetime.now(
        ).strftime('%Y-%m-%d'))
    tithe = fields.Selection(selection=[
        ('all', 'All'),
        ('members', 'Members'),
        ('pastor', 'Pastor'),
        ('minister', 'Minister')
    ], string='Category', default='all', required=True)

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

    def print_tithe_report(self, docids=None, data=None):
        """."""
        query = self.tithe
        church = ('church_id', '=', self.env.user.company_id.id)
        domain = [
            ('tithe_type', '=', query), church
        ] if self.tithe != 'all' else [church]
        tithes = self._report_range(self.env['ng_church.tithe_lines'].search(
            domain), self.date_from, self.date_to)
        if len(tithes) > 0:
            return self.env.ref(
                'ng_church.ng_church_tithe_line_report').report_action(
                tithes, data=data)
        raise MissingError('Record not found')
