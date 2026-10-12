from odoo import models, fields
from odoo.exceptions import UserError


class MealEmployeeReportWizard(models.TransientModel):
    _name = 'meal.employee.report.wizard'
    _description = 'Meal Employee Report Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def action_calculate(self):
        self.ensure_one()

        if self.date_from > self.date_to:
            raise UserError("Invalid date range.")

        cr = self.env.cr

        cr.execute("DROP VIEW IF EXISTS meal_employee_report")

        cr.execute("""
            CREATE OR REPLACE VIEW meal_employee_report AS (
                WITH package_expense AS (
                    SELECT
                        me.meal_package_id,
                        SUM(me.amount) AS total_amount
                    FROM meal_expanse me
                    WHERE me.date BETWEEN %s AND %s
                    GROUP BY me.meal_package_id
                ),
                package_meal AS (
                    SELECT
                        mp.id AS meal_package_id,
                        SUM(md.number_of_meal * mt.weightage) AS total_weighted_meal
                    FROM meal_daily md
                    JOIN meal_type mt ON mt.id = md.meal_type_id
                    JOIN meal_package mp ON mp.id = mt.meal_package_id
                    WHERE md.date BETWEEN %s AND %s
                    GROUP BY mp.id
                ),
                package_rate AS (
                    SELECT
                        pe.meal_package_id,
                        pe.total_amount / NULLIF(pm.total_weighted_meal, 0) AS meal_rate
                    FROM package_expense pe
                    JOIN package_meal pm
                        ON pm.meal_package_id = pe.meal_package_id
                ),
                -- Aggregate per EMPLOYEE only. Each line is priced with its
                -- own package rate first, so an employee eating across
                -- several packages collapses into a single row.
                employee_meal AS (
                    SELECT
                        md.employee_id AS employee_id,
                        COALESCE(SUM(md.number_of_meal_weightage), 0) AS total_meal,
                        COALESCE(SUM(
                            md.number_of_meal_weightage * COALESCE(pr.meal_rate, 0)
                        ), 0) AS total_bill
                    FROM meal_daily md
                    JOIN meal_type mt ON mt.id = md.meal_type_id
                    LEFT JOIN package_rate pr
                        ON pr.meal_package_id = mt.meal_package_id
                    WHERE md.date BETWEEN %s AND %s
                    GROUP BY md.employee_id
                ),
                -- Fixed monthly subsidy from the employee's assigned meal
                -- types. Percentage subsidies are already netted out of
                -- number_of_meal_weightage, so they are not added here.
                employee_subsidy AS (
                    SELECT
                        ma.employee_id,
                        COALESCE(SUM(mt.subsidy), 0) AS subsidy
                    FROM meal_assign ma
                    JOIN meal_assign_meal_type_rel rel
                        ON rel.meal_assign_id = ma.id
                    JOIN meal_type mt ON mt.id = rel.meal_type_id
                    WHERE mt.subsidy_type = 'fixed'
                    GROUP BY ma.employee_id
                )
                SELECT
                    row_number() OVER () AS id,
                    e.id AS employee_id,
                    em.total_meal AS total_meal,
                    CASE
                        WHEN em.total_meal <> 0 THEN em.total_bill / em.total_meal
                        ELSE 0
                    END AS meal_rate,
                    em.total_bill AS total_bill,
                    -- Subsidy can't exceed the bill.
                    LEAST(COALESCE(es.subsidy, 0), em.total_bill) AS subsidy,
                    em.total_bill
                        - LEAST(COALESCE(es.subsidy, 0), em.total_bill)
                        AS bill_after_subsidy
                FROM employee_meal em
                JOIN hr_employee e ON e.id = em.employee_id
                LEFT JOIN employee_subsidy es ON es.employee_id = em.employee_id
            )
        """, (
            self.date_from, self.date_to,
            self.date_from, self.date_to,
            self.date_from, self.date_to,
        ))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Meal Employee Report',
            'res_model': 'meal.employee.report',
            'view_mode': 'list',
            'target': 'current',
        }
