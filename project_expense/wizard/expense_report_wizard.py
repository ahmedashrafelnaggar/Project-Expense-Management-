from odoo import models, fields, api

class ExpenseReportWizard(models.TransientModel):
    _name = 'expense.report.wizard'
    _description = 'Project Expense Report Wizard'

    project_ids = fields.Many2many('project.project', string='Select Projects', required=True)

    def action_generate_report(self):
        """Generate the project expenses report."""
        return self.env.ref('project_expense.expense_request_report').report_action(self,data={'project_ids': self.project_ids.ids})