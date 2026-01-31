from odoo import models, fields, api
from odoo.exceptions import UserError

class MealDaily(models.Model):
    _name = 'meal.daily'
    _description = 'Daily Meal Record'
    _order = 'date desc'
    _rec_name = 'employee_id'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    meal_type_id = fields.Many2one('meal.type', string='Meal Type')
    number_of_meal = fields.Integer(string='Number of Meals', default=1)
    number_of_meal_weightage = fields.Float(string='Weighted Meals', compute='_compute_weighted_meals', store=True)
    department_id = fields.Many2one(
        'hr.department',
        compute='_compute_department',
        store=False
    )

    def _compute_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id


    @api.depends('meal_type_id', 'number_of_meal')
    def _compute_weighted_meals(self):
        for record in self:
            if record.meal_type_id and record.number_of_meal:
                if record.meal_type_id.subsidy_type == 'percentage':
                    record.number_of_meal_weightage = record.number_of_meal * record.meal_type_id.weightage * (1 - record.meal_type_id.subsidy / 100)
                else:
                    record.number_of_meal_weightage = record.number_of_meal * record.meal_type_id.weightage
            else:
                record.number_of_meal_weightage = 0.0

    