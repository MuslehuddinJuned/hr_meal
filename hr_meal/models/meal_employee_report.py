from odoo import models, fields, tools

class MealEmployeeReport(models.Model):
    _name = 'meal.employee.report'
    _description = 'Meal Employee Report'
    _auto = False

    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one(
        'hr.department',
        compute='_compute_department',
        store=False
    )

    total_meal = fields.Float(string='Total Meal')
    meal_rate = fields.Float(string='Meal Rate')
    total_bill = fields.Float(string='Total Bill')


    def _compute_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE VIEW meal_employee_report AS (
                SELECT
                    row_number() OVER () AS id,
                    e.id AS employee_id,
                    0::float AS total_meal,
                    0::float AS meal_rate,
                    0::float AS total_bill
                FROM hr_employee e
                WHERE FALSE
            )
        """)