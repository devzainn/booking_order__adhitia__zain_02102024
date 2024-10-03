from odoo import models, fields, api

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'New Modul of Moudle'

    name = fields.Char(string='WO Number', required=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('work.order'))
    booking_order_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='pending')
    notes = fields.Text(string='Notes')

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id:
            self.team_leader = self.team_id.team_leader
            self.team_members = self.team_id.team_members

    def action_start_work(self):
        self.write({
            'state': 'in_progress',
            'date_start': fields.Datetime.now()
        })

    def action_end_work(self):
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now()
        })

    def action_reset_work(self):
        self.write({
            'state': 'pending',
            'date_start': False
        })

    def action_cancel_work(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Work',
            'res_model': 'cancel.work.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

class CancelWorkWizard(models.TransientModel):
    _name = 'cancel.work.wizard'

    reason = fields.Text(string="Reason for Cancellation", required=True)

    def confirm_cancel(self):
        work_order = self.env['work.order'].browse(self._context.get('active_id'))
        work_order.write({
            'state': 'cancelled',
            'notes': work_order.notes + "\nCancellation Reason: " + self.reason if work_order.notes else "Cancellation Reason: " + self.reason
        })
    