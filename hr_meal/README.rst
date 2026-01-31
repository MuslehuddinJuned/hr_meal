=====================
HR Meal Management
=====================

This module provides a complete meal management system integrated with Odoo HR.
It allows organizations to define meal structures, assign meals to employees,
calculate daily meals, track meal expenses, and generate employee-wise meal costs
over configurable date ranges.



.. contents::
   :local:

Configuration
=============

The meal management process requires the following configurations:

Meal Packages
-------------
Meal packages define different categories of meals, such as staff meals,
officer meals, or management meals. Each package can have its own cost structure.

Meal Types
----------
Meal types represent individual meals such as breakfast, lunch, dinner, or snacks.
Each meal type is linked to a meal package and supports:
- Weightage
- Fixed or percentage subsidy

Meal Groups
-----------
Meal groups define meal schedules for employees. For example:
- Daily meals (including weekends)
- Weekday-only meals
- Custom working-day-based meals

Meal Assignment
---------------
Meals are assigned to employees by selecting:
- Employee
- Meal group
- Meal types

Each employee can have one active meal assignment.

Usage
=====

Calculate Meals
---------------
Meals can be calculated for:
- A single day
- Weekly
- Monthly
- Any custom date range

The calculation can be applied to:
- A single employee
- Selected employees
- All employees
- A specific meal group

Default meals are generated automatically. Any deviations (skipped meals,
additional meals, leave adjustments) can be edited manually.

Daily Meals
-----------
The Daily Meals menu provides a detailed view of all generated meals.
Users can review and adjust meals for any date range.

Meal Expenses
-------------
Meal-related expenses can be recorded with optional meal package assignment.
Expenses without a specific package are proportionally distributed across
all meals in the selected date range.

Employee Meal Cost
------------------
The system calculates:
- Total number of weighted meals
- Meal rate
- Employee-wise meal expense

This report can be generated for any date range.

Integration
===========

This module is designed to integrate with:
- HR Employees
- HR Contracts


Technical Information
=====================

* Model-driven architecture
* SQL-based reporting views for performance
* Compatible with Odoo 19
* No external Python dependencies

Known Limitations
=================

- Expenses are not linked to accounting modules
- Meal calculation assumes valid HR contracts

Roadmap
=======

- Multi-company enhancements
- Payroll rule integration
- Analytical accounting support

Bug Tracker
===========

Bugs are tracked on GitHub:
https://github.com/OCA/hr/issues

Credits
=======

Authors
-------

* ZachaiBachhai

Contributors
------------

* Muslehuddin Juned

Maintainers
-----------

This module is maintained by the OCA community.
