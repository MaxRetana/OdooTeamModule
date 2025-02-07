from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TeamModule(models.Model):
    _name = 'team.team'
    _description = 'Team Module'

    name = fields.Char(string='Name', required=True)
    
    _sql_constraints = [
        ('unique_team_name', 'UNIQUE(name)', 'The team name must be unique!')
    ]
    
    description = fields.Text(string='Description')
    team_leader_id = fields.Many2one('res.users', string='Team Leader')
    team_member_ids = fields.Many2many('res.partner', string='Team Members')
    
    @api.constrains('team_member_ids')
    def _check_team_member_ids(self):
        """Verifica que los miembros seleccionados no estén en otro equipo."""
        for record in self:
            name_members = []
            # Busca los miembros que ya están asignados a otro equipo (no el actual)
            for member in record.team_member_ids:
                # Verifica si el miembro está asignado a algún equipo, excluyendo el actual
                existing_teams = self.env['team.team'].search([
                    ('id', '!=', record.id),  # Excluir el equipo actual
                    ('team_member_ids', 'in', member.ids)  # Verifica si el miembro ya está en otros equipos
                ])
                if existing_teams:
                    name_members.append(member.name)  # Agrega el nombre del miembro a la lista

            if name_members:
                # Lanza un mensaje con los nombres de los miembros que ya están asignados
                raise ValidationError(_("The following members are already assigned to another team: %s") % ', '.join(name_members))
    
    team_size = fields.Integer(string='Team Size', compute='_compute_team_size', store=True)

    @api.depends('team_member_ids')
    def _compute_team_size(self):
      for record in self:
          if len(record.team_member_ids) > 0:
            record.team_size = len(record.team_member_ids) + 1
          else:
            record.team_size = 0
          