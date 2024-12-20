# Conventions

## Parameters
name : the name should be understandable by any one and follow the same scheme for the whole module. Also they should be coherent between modules as much as possible.
l10n : 2 character localization (e.g. BE)
employee_type : employee type (e.g. employee, worker, student)
struct_xml_id : xml id of the Salary Structure

## Record Ids
### Salary Structure
The default one should be called `l10n_[l10n]_regular_pay`.
Then all others should look like `l10n_[l10n]_[name]`.

e.g. l10n_ke_regular_pay, l10n_lu_13th_month_pay

n.b.
if you have multiple subcategories the convention become:
-The default one should be called `l10n_[l10n]_[categories]_regular_pay`.
-Then all others should look like `l10n_[l10n]_[categories]_[name]`.

e.g. l10n_be_cp200_regular_pay, l10n_be_cp200_13th_month_pay

### Structure Type
The default one should be called `l10n_[l10n]_[employee_type]`.
Then all others should look like `l10n_[l10n]_[employee_type]_[name]`.

e.g. l10n_ke_student, l10n_ke_employee_13th

n.b.
if you have multiple subcategories the convention become:
-The default one should be called `l10n_[l10n]_[categories]_[employee_type]`.
-Then all others should look like `l10n_[l10n]_[categories]_[employee_type]_[name]`.

e.g. l10n_be_cp200_student, l10n_be_cp200_employee_13th

### Input Types
The inputs should look like `l10n_[l10n]_input_[name]`.

e.g. l10n_ke_input_nhif

### Categories
The categories should look like `l10n_[l10n]_category_[name]`.

e.g. l10n_ke_category_basic

### Rule Parameters
The rule parameters should look like `l10n_[l10n]_rule_parameter_[name]`.

e.g. l10n_be_rule_parameter_onss

### Salary Rules
The salary rules should look like `[struct_xml_id]_[name]`

e.g. l10n_be_cp_200_regular_pay_basic

n.b.
- if the code is sufficiently explicit it's the preferred way to set `[name]` (lower(code))
- elif the name is sufficiently explicit it's the preferred way to set `[name]` (alphanumeric(name).replace(" ", "_"))
- else maybe you should rething the code and/or the name

### Work Entry Types
The work entry types should look like `l10n_[l10n]_work_entry_type_[name]`.

e.g. l10n_be_work_entry_type_attendance

### Leave Types
The leave types should look like `l10n_[l10n]_leave_type_[name]`.

l10n_be_leave_type_sick_leave

n.b.
- if the code is sufficiently explicit it's the preferred way to set `[name]` (lower(code))
- elif the name is sufficiently explicit it's the preferred way to set `[name]` (alphanumeric(name).replace(" ", "_"))
- else maybe you should rething the code and/or the name

## Record fields
### general
No referance to the current model should be written e.g. if you are in l10n_be_hr_payroll no record should be referenced like l10n_be_hr_payroll.l10n_be_input_basic but just be referenced as l10n_be_input_basic

### salary structure
A salary structure should have its field rule_ids set to `[]`. Don't use the default one or you'll not be able to translate them.

## Fields
All new fields for model existing in standard should start with `l10n_[l10n]_`.

## Models
New models for loca should start with `l10n.[l10n].` and the file should start with `l10n_[l10n]_`.
Fields inside those models don't need to start with `l10n_[l10n]_`.