from odoo import models, fields, api



class Project(models.Model):
    _inherit = 'project.project'

    expense_amount = fields.Float(string='Total Expense Amount', default=0.0)
    product_line_ids = fields.One2many('project.product.line', 'project_id', string='Product Lines')
    picking_id = fields.Many2one('stock.picking', string='Outgoing Picking')

    def action_view_picking(self):
        if self.picking_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Related Picking',
                'res_model': 'stock.picking',
                'res_id': self.picking_id.id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'current',  # Open in the same window
            }



class ProjectProductLine(models.Model):
    _name = 'project.product.line'
    _description = 'Project Product Line'

    project_id = fields.Many2one('project.project', required=True)
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id





