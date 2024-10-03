# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Model Service Team'
    
    name = fields.Char(string='Team Name', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')