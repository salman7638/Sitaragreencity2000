
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class BookingDiscountWizard(models.TransientModel):
    _name = "booking.discount.wizard"
    _description = "Booking Discount Wizard"
    

    discount = fields.Float(string='Disc(%)')
    sale_id = fields.Many2one('sale.order', string='Order')
    plot_ids = fields.Many2many('sale.order.line', string='Plots')
    
    
    
    def action_book_discount(self):
        if self.discount < 0:
            raise UserError('You are not allow to Enter Discount less than Zero!')

        if self.sale_id.installment_created==True:
            for installment_line in self.sale_id.installment_line_ids:
                if self.discount ==0:
                    installment_line.update({
                        'amount_residual': installment_line.total_actual_amount - installment_line.amount_paid,
                    })
                else:  
                    installment_line.update({
                        'amount_residual': installment_line.total_actual_amount - installment_line.amount_paid,
                    })
                    disc = ((installment_line.amount_residual/100) * self.discount)
                    installment_line.update({
                        'amount_residual': installment_line.amount_residual - disc,
                    })
                
        else:
            for line in self.plot_ids:
                line.update({
                    'discount':  self.discount,
                })
        self.sale_id.update({
            'disc': self.discount,
        })    