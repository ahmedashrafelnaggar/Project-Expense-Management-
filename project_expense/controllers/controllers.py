# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectExpense(http.Controller):
#     @http.route('/project_expense/project_expense/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_expense/project_expense/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_expense.listing', {
#             'root': '/project_expense/project_expense',
#             'objects': http.request.env['project_expense.project_expense'].search([]),
#         })

#     @http.route('/project_expense/project_expense/objects/<model("project_expense.project_expense"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_expense.object', {
#             'object': obj
#         })
