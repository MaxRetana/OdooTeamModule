{
  'name': 'Team Module',
  'version': '2.3',
  'author': 'Maximiliano Retana',
  'license': 'LGPL-3',  # Agrega una licencia (LGPL-3 es común para módulos de Odoo)
  'depends': ['base'],
  'data': [
    'security/ir.model.access.csv',
    'views/team_module_view.xml',
    # 'views/security.xml',
  ],
  'installable': True,
  'auto_install': False,
  'application': True,
}