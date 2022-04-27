# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    commission_date = fields.Date(string="Date")
    co_amount = fields.Float(string = "Commission Amount", compute ='_co_amount')
    
    @api.depends("price_subtotal","comission_amount","commission_type")
    def _co_amount(self):
        for line in self:
            if line.commission_type == 'percent':
                line.co_amount = ((line.price_subtotal/100)*line.comission_amount)
            elif line.commission_type == 'amount':
                line.co_amount = line.comission_amount
                
            else:
                line.co_amount = 0
                
                