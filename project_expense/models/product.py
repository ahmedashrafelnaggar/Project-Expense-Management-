from odoo import models, fields,api
from odoo.exceptions import ValidationError, UserError


class ProductLine(models.Model):
    _name = 'product.line'
    _description = 'Project Expense Product Line'

    request_id = fields.Many2one('project.expense.request', string='Expense Request', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")