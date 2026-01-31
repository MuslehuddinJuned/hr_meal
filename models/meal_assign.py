from odoo import api, models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if domain is None:
            domain = []

        # Check if the context flag is set (passed from the view)
        if self.env.context.get('exclude_assigned_for_meal'):
            # Find all employee IDs already assigned a meal
            assigned_employee_ids = self.env['meal.assign'].search([]).mapped('employee_id').ids

            if assigned_employee_ids:
                # Add the exclusion domain
                domain.append(('id', 'not in', assigned_employee_ids))

        # Call the super method with the new API
        return super().name_search(
            name=name,
            domain=domain,
            operator=operator,
            limit=limit
        )


class MealAssign(models.Model):
    _name = 'meal.assign'
    _description = 'Meal Assignment'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    meal_type_ids = fields.Many2many('meal.type', string='Meal Types')
    meal_group_id = fields.Many2one('meal.group', string='Meal Group')

    department_id = fields.Many2one(
        'hr.department',
        compute='_compute_department',
        store=False
    )

    def _compute_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id

    _name_unique = models.Constraint(
        'unique(employee_id)',
        "One employee can be assigned once!",
    )


class MealGroup(models.Model):
    _name = 'meal.group'
    _description = 'Meal Group'
    _rec_name = 'name'

    name = fields.Char(string='Meal Group', required=True)
    description = fields.Text(string='Description')

    _name_unique = models.Constraint(
        'unique(name)',
        "Meal Group must be unique!",
    )