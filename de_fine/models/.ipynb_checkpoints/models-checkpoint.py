# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date

class productProduct(models.Model):
    _inherit = "product.template"
    
    fine_amount = fields.Float(string="Fine Amount")
    
    
class OrderInstallmentLine(models.Model):
    _inherit = "order.installment.line"
    
    fine_amount = fields.Float(string="Fine Amount", compute='_compute_fine_amount')
    
    @api.depends("date","total_amount")
    def _compute_fine_amount(self):
        for line in self:
            today_date = date.today()
            if today_date > line.date:
#             raise UserErorr(date.today())
                fine_days=0
                f_date = date.today()
                l_date =line.date
                delta = f_date - l_date
                fine_days=delta.days
                line.fine_amount=(((((line.total_amount/100)*1)/365)*12)*fine_days) 
            else:
                line.fine_amount=0
            if line.fine_amount > 0 and line.remarks=='Pending':
                line.total_amount= line.fine_amount + line.total_amount  
                
                
                
                
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.model
    def add_fine_amount(self):
        for rec in self:
            total_fine_amount = 0
            for line in rec.installment_line_ids:
                if line.fine_amount > 0:
                    total_fine_amount += line.fine_amount
            rec.installment_amount_residual = total_fine_amount + rec.installment_amount_residual
                
                