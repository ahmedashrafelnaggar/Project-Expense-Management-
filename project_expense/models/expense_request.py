from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError



class ProjectExpenseRequest(models.Model):
    _name = 'project.expense.request'
    _description = 'Project Expense Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Fields for the Expense Request
    name = fields.Char(string="Reference", required=True, copy=False, default='Ahmed')
    date = fields.Date(string='Date', default=fields.Date.today())
    project_id = fields.Many2one('project.project', string='Project', domain=[('active', '=', True)])
    project_manager_id = fields.Many2one('res.users', string='Project Manager', readonly=True)
    line_ids = fields.One2many('project.expense.request.line', 'expense_request_id', string='Expense Types')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='State', default='draft', tracking=True)
    total_amount = fields.Float(compute='_compute_total_amount', store=True)
    task_count = fields.Integer('Number of Tasks', compute='_compute_task_count', store=True)
    date_deadline = fields.Datetime(string="Deadline")
    request_date = fields.Datetime(string="Request Date")
    user_id = fields.Many2one('res.users', string="User")
    priority = fields.Selection(
        [
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        string='Priority',
        default='1',
    )
    kanban_state = fields.Selection([("draft", "مسودة"), ("done", "منجز")])
    member_id = fields.Many2one('res.partner', string='Member', help='The member who made the checkout')

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for req in self:
            req.total_amount = sum(line.amount for line in req.line_ids)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.project_manager_id = self.project_id.user_id if self.project_id else False

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_approved(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'
        self.project_id.expense_amount += sum(self.line_ids.mapped('amount'))
        self.create_delivery_order()


    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise UserError("You cannot delete a record in the 'Done' state.")
        return super(ProjectExpenseRequest, self).unlink()

    def copy(self, default=None):
        for record in self:
            if record.state == 'done':
                raise UserError("You cannot copy an expense request that is in the 'Done' state.")
        return super(ProjectExpenseRequest, self).copy(default)

    def create_delivery_order(self):
        StockPicking = self.env['stock.picking']
        StockMove = self.env['stock.move']

        for record in self:
            picking = StockPicking.create({
                'partner_id': record.project_id.partner_id.id,
                'picking_type_id': self.env.ref('stock.picking_type_out').id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                'origin': record.name,
            })

            for line in record.product_line_ids:
                StockMove.create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'picking_id': picking.id,
                })

            record.picking_id = picking.id


    def open_wizard(self):
        action = self.env.ref('project_expense.action_project_expense_report_wizard').read()[0]
        return action

    def open_picking(self):
        """Return an action to open the related stock picking."""
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
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'No Picking Found',
                'res_model': 'project.expense.request',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'current',
                'context': {'message': 'No related picking found for this expense request.'},
            }

    @api.constrains('line_ids')
    def _check_line_amounts(self):
        for line in self.line_ids:
            if line.amount <= 0:
                raise ValidationError("Amount must be greater than 0.")
            if line.amount > line.expense_type_id.limit:
                raise ValidationError("Amount exceeds the type's limit.")


class ProjectExpenseRequestLine(models.Model):
    _name = 'project.expense.request.line'
    _description = 'Project Expense Request Line'

    expense_request_id = fields.Many2one('project.expense.request', string="Expense Request", required=True)
    product_id = fields.Many2one('product.product', required=True)
    expense_type_id = fields.Many2one('expense.type', string='Expense Type', required=True)
    amount = fields.Float(string='Amount', required=True)
    quantity = fields.Float(required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')

    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount <= 0:
                raise ValidationError("Amount must be greater than 0.")
            if line.amount > line.expense_type_id.limit:
                raise ValidationError("Amount exceeds the type's limit.")
