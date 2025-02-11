from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExpenseType(models.Model):
    _name = 'expense.type'
    _description = 'Expense Type'

    name = fields.Char(string="Expense Type Name", required=True)
    limit = fields.Float(string="Limit", required=True, default=1.0)

    @api.constrains('limit')
    def _check_limit(self):
        for record in self:
            if record.limit <= 0:
                raise ValidationError("Limit must be greater than 0.0")
