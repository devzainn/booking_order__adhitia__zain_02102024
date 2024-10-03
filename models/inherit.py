# from xml.dom import ValidationErr
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string='Is Booking Order',default=False)
    team_id = fields.Many2one('service.team', string='Team')
    team_leader = fields.Many2one('res.users', string='Team Leader')
    team_members = fields.Many2many('res.users', string='Team Members')
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')

    @api.model
    def create(self, vals):
        if vals.get('booking_start') or vals.get('booking_end'):
            vals['is_booking_order'] = True
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if 'booking_start' in vals or 'booking_end' in vals:
            vals['is_booking_order'] = True
        return super(SaleOrder, self).write(vals)

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id:
            self.team_leader = self.team_id.team_leader    
            self.team_members = [(6, 0, self.team_id.team_members.ids)]
        else:
            self.team_leader = False
            self.team_members = False

    # @api.onchange('team_id')
    # def _onchange_team_id(self):
    #     if self.team_id:
    #         self.team_leader = self.team_id.team_leader
    #         self.team_members = self.team_id.team_members

    @api.multi
    def check_availability(self):
        overlap_orders = self.env['work.order'].search([
            ('team_id', '=', self.team_id.id),
            ('state', '!=', 'cancelled'),
            ('planned_start', '<=', self.booking_end),
            ('planned_end', '>=', self.booking_start),
        ])
        if overlap_orders:
            raise ValidationError("Team already has work order during that period on SO")
        # return self.env['ir.actions.act_window'].display_popup('Team is available for booking')
        

    # @api.multi
    # def action_confirm(self):
    #     self.ensure_one()
    #     overlap_orders = self.env['work.order'].search([
    #         ('team_id', '=', self.team_id.id),
    #         ('state', '!=', 'cancelled'),
    #         ('planned_start', '<=', self.booking_end),
    #         ('planned_end', '>=', self.booking_start),
    #     ])
    #     if overlap_orders:
    #         raise ValidationErr(f"Team is not available during this period, already booked on SO{overlap_orders[0].booking_order_id.id}")
        
    #     work_order = self.env['work.order'].create({
    #         'booking_order_id': self.id,
    #         'team_id': self.team_id.id,
    #         'team_leader': self.team_leader.id,
    #         'team_members': [(6, 0, self.team_members.ids)],
    #         'planned_start': self.booking_start,
    #         'planned_end': self.booking_end,
    #         'state': 'pending'
    #     })
    #     return super(SaleOrder, self).action_confirm()
    
    