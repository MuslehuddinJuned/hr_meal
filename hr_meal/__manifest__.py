
{
    'name': 'Meal Management',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': """
            Enables meal structure management, employee meal assignment, daily meal calculation, expense tracking, and employee-wise cost reporting by date range.
        """,
    'description': 'Module to manage meals for employees including types, assignments, daily consumption, and expenses',
    'author': 'Musleh Uddin Juned',
    'website': 'http://www.zachai-bachhai.com',
    'depends': ['base', 'hr', 'mail', 'product', 'uom'],
    'data': [
        # 'security/meal_security.xml',
        'security/ir.model.access.csv',
        'views/meal_type_views.xml',
        'views/meal_assign_views.xml',
        'views/meal_daily_views.xml',
        'views/meal_expanse_views.xml',
        'views/wizard_meal_calculate_views.xml',
        'views/meal_employee_report_views.xml',
        'views/meal_employee_report_wizard_views.xml',
        'views/meal_menus.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}