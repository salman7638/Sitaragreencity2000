# -*- coding: utf-8 -*-

from odoo import models, fields, api

class productProduct(models.Model):
    _inherit = "product.template"
    _description = "Product Product"
    fine_amount = fields.Char(string="Fine Amount")
    
    
class SaleOrder(models.Model):
    _inherit = "order.installment.line"
    _description = "Sale Order"
    fine_amount = fields.Char(string="Fine Amount")