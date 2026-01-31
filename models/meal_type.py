from odoo import models, fields

class MealType(models.Model):
    _name = 'meal.type'
    _description = 'Meal Type'
    _rec_name = 'name'

    name = fields.Char(string='Meal Type', required=True)
    description = fields.Text(string='Description')
    weightage = fields.Float(string='Weightage', help='Weightage for this meal type. If this kind of meal is not related to regullar expense, keep it 0')
    is_active = fields.Boolean(string='Is Active', default=True)
    subsidy_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string='Subsidy Type', default='fixed')
    subsidy = fields.Float(string='Subsidy', help='Subsidy amount for this meal type')
    meal_package_id = fields.Many2one('meal.package', string='Meal Package')
    
    _name_unique = models.Constraint(
        'unique(name)',
        "Meal Type must be unique!",
    )


class MealPackage(models.Model):
    _name = 'meal.package'
    _description = 'Meal Package'
    _rec_name = 'name'

    name = fields.Char(string='Meal Package', required=True)
    description = fields.Text(string='Description')
    meal_type_ids = fields.Many2many('meal.type', string='Meal Types')
    is_active = fields.Boolean(string='Is Active', default=True)

    _name_unique = models.Constraint(
        'unique(name)',
        "Meal Package must be unique!",
    )