from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string='Is Booking Order',default=False)
    team_new_id = fields.Many2one('service.team', string='Team', required=False)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=False)
    team_members = fields.Many2many('res.users', string='Team Members', required=False)
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')

    @api.onchange('team_new_id')
    def _onchange_team_id(self):
        if self.team_id:
            self.team_leader = self.team_new_id.team_leader
            self.team_members = self.team_new_id.team_members

    def check_team_availability(self):
        if not self.booking_start or not self.booking_end:
            raise UserError(_("Please set the booking start and end dates."))

        domain = [
            ('team_id', '=', self.team_new_id.id),
            ('state', '!=', 'cancelled'),
            '|', 
            '&', ('planned_start', '<=', self.booking_end), ('planned_start', '>=', self.booking_start),
            '&', ('planned_end', '>=', self.booking_start), ('planned_end', '<=', self.booking_end)
        ]

        overlapping_work_orders = self.env['work.order'].search(domain)

        if overlapping_work_orders:
            work_order = overlapping_work_orders[0]
            raise UserError(_(
                "Team already has a work order during that period on Booking Order: %s" % work_order.booking_order_id.name
            ))
        else:
            raise UserError(_("Team is available for booking"))

    def _check_team_availability(self):
        if not self.booking_start or not self.booking_end:
            raise UserError(_("Please set the booking start and end dates."))

        domain = [
            ('team_id', '=', self.team_new_id.id),
            ('state', '!=', 'cancelled'),
            '|', 
            '&', ('planned_start', '<=', self.booking_end), ('planned_start', '>=', self.booking_start),
            '&', ('planned_end', '>=', self.booking_start), ('planned_end', '<=', self.booking_end)
        ]

        overlapping_work_orders = self.env['work.order'].search(domain)

        if overlapping_work_orders:
            return overlapping_work_orders

    def action_confirm_booking_sale_order(self):
        if not self.booking_start or not self.booking_end:
            raise UserError(_("Please set the booking start and end dates."))

        overlapping_work_orders = self._check_team_availability()

        if overlapping_work_orders:
            work_order = overlapping_work_orders[0]
            raise UserError(_(
                "Team is not available during this period, already booked on %s. "
                "Please book on another date." % work_order.booking_order_id.name
            ))

        work_order_vals = {
            'booking_order_id': self.id,
            'team_id': self.team_new_id.id,
            'team_leader': self.team_leader.id,
            'team_members': [(6, 0, self.team_members.ids)],
            'planned_start': self.booking_start,
            'planned_end': self.booking_end,
            'state': 'pending',
        }
        work_order = self.env['work.order'].create(work_order_vals)

        self.work_order_id = work_order.id

        return super(SaleOrder, self).action_confirm()

    @api.model
    def create(self, vals):
        if 'team_new_id' in vals:
            team = self.env['service.team'].browse(vals['team_new_id'])
            vals['team_leader'] = team.team_leader.id
            vals['team_members'] = [(6, 0, team.team_members.ids)]
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if 'team_new_id' in vals:
            team = self.env['service.team'].browse(vals['team_new_id'])
            vals['team_leader'] = team.team_leader.id
            vals['team_members'] = [(6, 0, team.team_members.ids)]
        return super(SaleOrder, self).write(vals)