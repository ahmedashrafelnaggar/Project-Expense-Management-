from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http



class ExpensePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        rtn = super(ExpensePortal,self)._prepare_home_portal_values(counters)
        print("_prepare_home_portal_values....",rtn)
        rtn['request_counts'] = request.env['project.expense.request'].search_count([])
        return rtn

    @http.route(['/my/expense_requests'], type='http',website=True)
    def ExpenseListView(self,**kw):
        requests = request.env['project.expense.request'].search([])
        vals = {
            'requests': requests,
            'page_name':'request_list_view',

        }
        return request.render('project_expense.portal_my_expenses',vals)


    @http.route(['/my/expense_requests<model("project.expense.request"):request_id>'], type='http', website=True)
    def ExpenseFormView(self,request_id,**kw):
        print("hello /my/partner ")

        vals = {
            'Requests': request_id,
            'page_name':'request_form_view',

        }
        return request.render('project_expense.portal_expense_form',vals)


