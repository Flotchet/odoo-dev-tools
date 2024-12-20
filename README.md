# Odoo Dev Tools

This repo is made to put together different scripts used to make the developper life at odoo easier

## Naming Conventions
### Structure
The default one should be called `l10n_xx_regular_pay`.
Then all others should look like `l10n_xx_yyyyyyyy`.

### Structure Type
The default one should be called `l10n_xx_employee`.
Then all others should look like `l10n_xx_yyyyyyyy`.

### Input Types
The inputs should look like `l10n_xx_input_yyyyyyyy`.

### Categories
The categories should look like `l10n_xx_category_yyyyyyyy`.

### Rule Parameters
The rule parameters should look like `l10n_xx_rule_parameter_yyyyyyyy`.

### Salary Rules
The salary rules should look like `l10n_xx_regular_pay_yyyyyyyy` where we replace `regular_pay` by whatever the structure is.

### Work Entry Types
The work entry types should look like `l10n_xx_work_entry_type_yyyyyyyy`.

### Leave Types
The leave types should look like `l10n_xx_leave_type_yyyyyyyy`.


## hr_salary_rules_xml_checker

This is a script that will automatically reformat a xml file to respect the code standard of R&D for hr salary rules record


- Usage: python3 hr_salary_rules_xml_checker.py < path:file.xml >[y/n][y/i/n]
- arg1: path to the xml file
- arg2: remove data tag  (y/n) (y: yes, n: no)
- arg3: fully reformat the xml file (y/i/n)(y: yes, i: insert, n: no) 
