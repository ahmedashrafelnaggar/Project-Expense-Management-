# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class project_expense(models.Model):
#     _name = 'project_expense.project_expense'
#     _description = 'project_expense.project_expense'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
