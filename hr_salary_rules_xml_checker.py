from os.path import exists
from re import compile as re_compile, Pattern
from sys import argv, exit as sys_exit
from typing import Union, List
from xml.etree import ElementTree as ET

order_tag = 'sequence'

str_or_none: type = Union[str, None]
node_type: type = ET.Element

CODE_ID_MAX_LENGTH: int = 32
STRUCT_ID_MAX_LENGTH: int = 64

code_id_format: Pattern = re_compile(r'^[A-Za-z0-9_.]+$')
struct_id_format: Pattern = re_compile(r'^l10n_[a-z]{2}_[a-z_.]+$')


class FormatError(Exception):
    pass


class colors:
    OKBLUE: str = '\033[94m'
    OKCYAN: str = '\033[96m'
    OKGREEN: str = '\033[92m'
    WARNING: str = '\033[93m'
    FAIL: str = '\033[91m'
    ENDC: str = '\033[0m'


def validate_and_reformat_xml_ids(
    file_path: str,
    remove_data: str_or_none = None,
    fully_reformat: str_or_none = None,
):

    tree: ET = ET.parse(file_path)
    root: node_type = tree.getroot()
    root = check_data_tags(root, remove_data)

    fully_reformat: str = fully_reformat or input(
        f'Do you want to fully reformat the xml file ? {colors.WARNING}(y/i/n){colors.ENDC} (y: yes, i: instert, n: no)'
    )
    assert fully_reformat.lower() in ['y', 'i', 'n'], f'{colors.FAIL}FAIL:{colors.ENDC} invalid input {fully_reformat}'

    is_ordered = assess_order_values(root)

    if fully_reformat.lower() == 'i':
        file_content: str = get_file_content(file_path)

    for record in root.findall(".//record"):
        if not (old_xml_id := node_to_hr_salary_rule_xml_id(record)):
            continue

        if old_xml_id == (new_id := node_to_conventionalized_hr_salary_rule_xml_id(record, file_path)):
            print(f'{colors.OKGREEN}INFO:{colors.ENDC} xml id {old_xml_id} is already correct')
            continue

        if fully_reformat == 'i':
            file_content = file_content.replace(f'id="{old_xml_id}"', f'id="{new_id}"')
            print(f'{colors.OKCYAN}INFO:{colors.ENDC} Changing xml id {old_xml_id} to {new_id} because it is not respecting the convention')
            continue

        record.set('id', new_id)
        print(f'{colors.OKCYAN}INFO:{colors.ENDC} Changing xml id {old_xml_id} to {new_id} because it is not respecting the convention')

    if fully_reformat.lower() == 'y':
        write_xml_reformated(file_path, tree, is_ordered)

    elif fully_reformat.lower() == 'i':
        write_file_content(file_path, file_content)


def assess_order_values(node: node_type):
    order_values: List[str] = [order_values.text for order_values in node.findall(f'.//{order_tag}')]

    if not all(order_values):
        print(f'{colors.WARNING}WARNING:{colors.ENDC} sequence order is not set in the xml file')
    elif not all(order.isdigit() for order in order_values):
        print(f'{colors.WARNING}WARNING:{colors.ENDC} sequence order is not in digits in the xml file')

    order_values = [int(order) for order in order_values if order.isdigit()]

    if order_values != sorted(order_values):
        print(f'{colors.WARNING}WARNING:{colors.ENDC} sequence order is not in order in the xml file')
        return False
    return True


def get_file_content(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        content: str = file.read()
    return content


def write_file_content(file_path: str, content: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'{colors.OKGREEN}SUCCESS: Writing changes to file done{colors.ENDC}')


def write_xml_reformated(file_path: str, tree: ET, is_ordered: bool):
    print(f'{colors.OKCYAN}INFO:{colors.ENDC} Writing changes to {file_path} ...')
 
    if not is_ordered:
        root: node_type = tree.getroot()
        records: List[node_type] = root.findall('.//record')
        for record in records:
            root.remove(record)
        records = sorted(records, key=lambda x: x.find(order_tag).text)
        for record in records:
            root.append(record)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


    print(f'{colors.OKGREEN}SUCCESS: bare xml changes written to file{colors.ENDC}')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines: List[str] = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if '<?xml version="1.0" encoding="utf-8"?>' in line:
                file.write('<?xml version="1.0" encoding="utf-8"?>')
                continue

            if '" />' in line:
                file.write(line.replace('" />', '"/>'))
                continue

            file.write(line)

    print(f'{colors.OKGREEN}SUCCESS: Writing changes to file done{colors.ENDC}')


def node_to_conventionalized_hr_salary_rule_xml_id(node: node_type, file_path: str):
    code: str = node_to_hr_salary_rule_code(node, file_path)
    formated_code: str = code.replace(".", "_")
    struct_id: str = node_to_hr_salary_rule_struct_id(node)
    formated_struct_id: str = struct_id.split('.')[-1]
    return f'{formated_struct_id}_{formated_code}'.lower()


def node_to_hr_salary_rule_struct_id(node: node_type):
    struct_id: str_or_none = node.find(".//field[@name='struct_id']").get('ref')
    if not struct_id:
        raise FormatError(f'{colors.FAIL}FAIL:{colors.ENDC} struct_id: {struct_id} is missing')
    if not struct_id_format.match(struct_id):
        raise FormatError(f'{colors.FAIL}FAIL:{colors.ENDC} struct_id: {struct_id} does not respect the format {struct_id_format.pattern}')
    if len(struct_id) > STRUCT_ID_MAX_LENGTH:
        print(f'{colors.WARNING}WARNING:{colors.ENDC} warning struct_id: {struct_id} is too long')
    return struct_id


def node_to_hr_salary_rule_code(node: node_type, file_path: str):
    code: str_or_none = node.find(".//field[@name='code']").text
    if not code:
        raise FormatError(f'{colors.FAIL}FAIL:{colors.ENDC} code: {code} is missing')
    if not code_id_format.match(code) and 'l10n_' in file_path:
        raise FormatError(f'{colors.FAIL}FAIL:{colors.ENDC} code: {code} does not respect the format {code_id_format.pattern}')
    if len(code) > CODE_ID_MAX_LENGTH:
        print(f'{colors.WARNING}WARNING:{colors.ENDC} code: {code} is too long')
    return code


def node_to_hr_salary_rule_xml_id(node: node_type):
    if not (xml_id := node.get('id')):
        return False
    if node.get('model') != 'hr.salary.rule':
        return False
    return xml_id


def check_data_tags(root: node_type, remove_data: str_or_none = None):
    for data in root.findall('.//data'):
        if data.get('noupdate'):
            continue

        print(f'{colors.WARNING}WARNING:{colors.ENDC} NO UPDATE IS NOT SET THE DATA TAG IS NOT NEEDED')
        key: str = remove_data or input(f'Do you want to remove the data tag? {colors.WARNING}(y/n){colors.ENDC} (y: yes, n: no)')
        assert key.lower() in ['y', 'n'], f'{colors.FAIL}FAIL:{colors.ENDC} invalid input {key}'

        if key.lower() == 'y':
            root.remove(data)
            print(f'{colors.OKCYAN}INFO:{colors.ENDC} data tag removed')
            continue

        print(f'{colors.OKCYAN}INFO:{colors.ENDC} data tag not removed')
    return root


def helper():
    print(f'{colors.WARNING}Usage:{colors.ENDC} python3 change.py {colors.OKBLUE}<path:file.xml>{colors.ENDC}')
    print(f'{colors.WARNING}Usage:{colors.ENDC} python3 change.py {colors.OKBLUE}<path:file.xml>{colors.ENDC} {colors.OKCYAN}[y/n]{colors.ENDC} {colors.OKGREEN}[y/i/n]{colors.ENDC}')
    print(f'{colors.OKBLUE}arg1:{colors.ENDC} path to the xml file')
    print(f'{colors.OKBLUE}arg2:{colors.ENDC} remove data tag {colors.WARNING}(y/n){colors.ENDC} (y: yes, n: no)')
    print(f'{colors.OKBLUE}arg3:{colors.ENDC} fully reformat the xml file {colors.WARNING}(y/i/n){colors.ENDC} (y: yes, i: instert, n: no)')


def main():
    if len(argv) not in [2, 3, 4]:
        helper()
        sys_exit(1)

    file_path: str = argv[1]
    if not exists(file_path):
        print(f'{colors.FAIL}FATAL ERROR: File not found: {file_path}{colors.ENDC}')
        sys_exit(1)

    try:
        validate_and_reformat_xml_ids(file_path, *argv[2:])
    except FormatError as e:
        raise e
    except Exception as e:
        print(f'{colors.FAIL}FATAL ERROR: {e}{colors.ENDC}') 
        helper()
        sys_exit(1)


if __name__ == '__main__':
    main()