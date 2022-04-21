
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
        payment_list=[]
        for line in self.product_ids:
            resell_vals={
                'partner_id': self.reseller_id.id,
                'customer_id': self.partner_id.id,
                'date': self.resell_date,
                'product_id': line.product_tmpl_id.id,
                'amount_paid': line.amount_paid,
                'amount_residual': line.amount_residual,
            }
            reseller = self.env['uniq.reseller.line'].create(resell_vals)
            line.update({
                'partner_id': self.partner_id.id,
            }) 
            for pay in line.payment_ids:
                payment_list.append(pay.id)
                
            for booking_line  in  line.booking_id.order_line:
                if booking_line.product_id.id==line.id:
                   booking_line.unlink() 
        booking_vals = {
            'partner_id': self.partner_id.id,
            'date_order': self.resell_date,
        }
        booking = self.env['sale.order'].create(booking_vals)
        for prd_line in self.product_ids:
            prd_line.update({
                'booking_id': booking.id,
            })
            
            line_vals = {
                'order_id': booking.id,
                'product_id': prd_line.id,
                'price_unit':  prd_line.list_price,
            }
            booking_line = self.env['sale.order.line'].create(line_vals)             
        payments=self.env['account.payment'].search([('id','in', payment_list)])        
         
        for pay_line in payments:
            pay_line.action_draft()
            pay_line.update({
                'partner_id': self.partner_id.id,
                'order_id': booking.id,
            })
            pay_line.action_post()