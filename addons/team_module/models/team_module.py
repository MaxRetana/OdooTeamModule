from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TeamModule(models.Model):
    _name = 'team.team'
    _description = 'Team Module'

    name = fields.Char(string='Name', required=True)
    
    _sql_constraints = [
        ('unique_team_name', 'UNIQUE(name)', 'The team name must be unique!')
    ]

    # @api.model
    # def create(self, vals):
    #     """Si el nombre ya existe, le agrega un número incremental sin mostrar error."""
    #     if 'name' in vals:
    #         base_name = vals['name']
    #         counter = 1
    #         while self.search([('name', '=', vals['name'])]):
    #             vals['name'] = f"{base_name} {counter}"
    #             counter += 1

    #     return super().create(vals)

    # @api.constrains('name')
    # def _check_unique_name(self):
    #     """Valida que el nombre sea único para evitar errores con la restricción SQL."""
    #     for record in self:
    #         existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
    #         if existing:
    #             raise ValidationError(_('The team name must be unique!'))
    
    description = fields.Text(string='Description')
    team_leader_id = fields.Many2one('res.users', string='Team Leader')
    team_member_ids = fields.Many2many('res.partner', string='Team Members')
    team_size = fields.Integer(string='Team Size', compute='_compute_team_size', store=True)

    @api.depends('team_member_ids')
    def _compute_team_size(self):
      for record in self:
          if len(record.team_member_ids) > 0:
            record.team_size = len(record.team_member_ids) + 1
          else:
            record.team_size = 0