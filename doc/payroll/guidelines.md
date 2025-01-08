# Guidelines

## Glossary
- `name` : the name should be understandable by any one and follow the same scheme for the whole module. Also they should be coherent between modules as much as possible.
- `country` : 2 character localization (e.g. be)
- `employee_type` : employee type (e.g. employee, worker, student)
- `struct_xml_id` : xml id of the Salary Structure

## Record Ids
### Salary Structure

- The default one should be called `l10n_[country]_regular_pay`.
- Then all others should look like `l10n_[country]_[name]`.

_Example:_ `l10n_ke_regular_pay`, `l10n_lu_13th_month`

If you have multiple subcategories the convention become:
- The default one should be called `l10n_[country]_[categories]_regular_pay`.
- Then all others should look like `l10n_[country]_[categories]_[name]`.

_Example:_ `l10n_be_cp200_regular_pay`, `l10n_be_cp200_13th_month`

### Structure Type

- The default one should be called `l10n_[country]_[employee_type]`.
- Then all others should look like `l10n_[country]_[employee_type]_[name]`.

_Example:_ `l10n_ke_student`, `l10n_ke_employee`

If you have multiple subcategories the convention become:
- The default one should be called `l10n_[country]_[categories]_[employee_type]`.
- Then all others should look like `l10n_[country]_[categories]_[employee_type]_[name]`.

_Example:_ `l10n_be_cp200_employee`, `l10n_be_cp200_pfi_employee`

### Input Types
The inputs should look like `l10n_[country]_input_[name]`.

_Example:_ `l10n_ke_input_nhif`

### Categories
The categories should look like `l10n_[country]_category_[name]`.

_Example:_ `l10n_ke_category_basic`

### Rule Parameters
The rule parameters should look like `l10n_[country]_rule_parameter_[name]`.

_Example:_ `l10n_be_rule_parameter_onss`

### Salary Rules
The salary rules should look like `[struct_xml_id]_[name]`

All salary rules should also be ordered by their sequence number in the file.

_Example:_ `l10n_be_cp200_regular_pay_basic`

**Important:**
- if the code is sufficiently explicit it's the preferred way to set `[name]` (lower(code))
- elif the name is sufficiently explicit it's the preferred way to set `[name]` (alphanumeric(name).replace(" ", "_"))
- else maybe you should rethink the code and/or the name

n.b. the code should be consider as an user friendly id for the rule so it should preferrably not contain space and be understandable by some kind of logic

### Work Entry Types
**All work entries should be defined in the `hr_work_entry` module to allow them to be used without payroll installed.**

The work entry types should look like `l10n_[country]_work_entry_type_[name]`.

_Example:_ `l10n_be_work_entry_type_attendance`

### Leave Types
**All leave types should be defined in the `hr_holidays` module to allow them to be used without payroll installed.**

The leave types should look like `l10n_[country]_leave_type_[name]`.

_Example:_ `l10n_be_leave_type_sick_leave`

**Important:**
- if the code is sufficiently explicit it's the preferred way to set `[name]` (lower(code))
- elif the name is sufficiently explicit it's the preferred way to set `[name]` (alphanumeric(name).replace(" ", "_"))
- else maybe you should rethink the code and/or the name


## Record Existing Fields
### General
No referance to the current model should be written e.g. if you are in `l10n_be_hr_payroll` no record should be referenced like `l10n_be_hr_payroll.l10n_be_input_basic` but just be referenced as `l10n_be_input_basic`.

### Salary Structure
A salary structure should have its field `rule_ids` set to `[]`. Don't use the default one or you wont be able to translate them.

## Fields
All new fields for model existing in standard should start with `l10n_[country]_`.

Also the `string` of those fields should always be `"[country]: [name]"`.
Then in the views, the string should be overriden to `"[name]"`.

This is to avoid the runbot unhappy about fields with same labels (could happen if different localisations are installed at the same time).

## Models
New models for loca should start with `l10n.[country].` and the file should start with `l10n_[country]_`.
Fields inside those models don't need to start with `l10n_[country]_`.
