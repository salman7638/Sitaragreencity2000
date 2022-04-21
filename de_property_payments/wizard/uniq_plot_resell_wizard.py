
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class UniqPlotResellWizard(models.TransientModel):
    _name = "uniq.plot.resell.wizard"
    _description = "Uniq Plot Resell wizard"
    

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    reseller_id = fields.Many2one('res.partner', string='Reseller')
    resell_date = fields.Date(string='Reselling Date',  required=True, default=fields.date.today())
    product_ids = fields.Many2many('product.product', string='Products')

    def action_confirm(self):
        resell_vals={
            'partner_id': self.reseller_id.id,
            'customer_id': self.partner_id.id,
            'date': self.resell_date,
            'order_id': self.sale_id.id,
            'amount_paid': self.sale_id.amount_paid,
            'amount_residual': self.sale_id.amount_residual,
        }
        reseller = self.env['uniq.plot.reseller.line'].create(resell_vals)
        self.product_id.update({
            'partner_id': self.partner_id.id,
        })     
                     
        