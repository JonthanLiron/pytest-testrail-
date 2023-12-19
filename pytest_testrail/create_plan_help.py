import json
from typing import Dict


TR_PLAN_HELP_JSON = "tr_help.json"
TR_PROJECT_HELP_JSON = "tr_project_help.json"


def extract_function_name(s: str) -> str:
    # Remove the enclosing brackets
    s = s.strip('<>')

    # Remove the 'Function ' part
    s = s.replace('Function ', '')

    return s


def draw_square_around_text_with_indent(text: str, indent: str) -> str:
    text = extract_function_name(text)
    # Characters for drawing the box
    top_left = '┌'  # Hex value: 0xC9 in Extended ASCII
    top_right = '┐'  # Hex value: 0xBB
    bottom_left = '└'  # Hex value: 0xC8
    bottom_right = '┘'  # Hex value: 0xBC
    horizontal = '─'  # Hex value: 0xCD
    vertical = '│'  # Hex value: 0xBA

    # Length of the text
    text_length = len(text)

    # Top border
    top_border = indent + top_left + horizontal * (text_length + 2) + top_right
    # Bottom border
    bottom_border = indent + bottom_left + horizontal * (text_length + 2) + bottom_right

    # Prepare the string with the box
    boxed_text = top_border + '\n'
    boxed_text += indent + vertical + ' ' + text + ' ' + vertical + '\n'
    boxed_text += bottom_border

    return boxed_text


def middle_test_string(test: Dict[str, str]) -> str:
    mid_connector = "├── "
    mid_pipe      = "│   "

    help_str = f'{mid_connector}{test["title"]}\n'
    help_str = f'{help_str}{mid_pipe}test_id: {test["id"]}\n'
    help_str = f'{help_str}{mid_pipe}case_id: {test["case_id"]}\n'
    test_name = test.get('test')
    if test_name is not None:
        boxed_string = draw_square_around_text_with_indent(
            text=f'{test_name}',
            indent=f'\x00{mid_pipe}')
        help_str = f'{help_str}{boxed_string}\n'
    help_str = f'{help_str}{mid_pipe}\n'
    return help_str


def last_test_string(test: Dict[str, str]) -> str:
    end_connector = "└── "
    empty         = "    "
    help_str = f'{end_connector}{test["title"]}\n'
    help_str = f'{help_str}\x00{empty}test_id: {test["id"]}\n'
    help_str = f'{help_str}\x00{empty}case_id: {test["case_id"]}\n'
    test_name = test.get('test')
    if test_name is not None:
        boxed_string = draw_square_around_text_with_indent(
            text=f'{test_name}',
            indent=f'\x00{empty}')
        help_str = f'{help_str}{boxed_string}\n'
    help_str = f'{help_str}\x00\x00\n\x00\n'
    return help_str


def help_tr_create_plan_json() -> str:
    try:
        with open(TR_PLAN_HELP_JSON, "r") as input_file:
            data = json.load(input_file)
        #help_str = json.dumps(data, indent=4)
        help_str = 'Create JSON help file for TestRail plan specified by option "--tr-plan-id"\n\x00\n'
        for run_test in data:
            help_str = f'{help_str}{run_test["name"]}\nrun_id: {run_test["id"]}\n'
            last_test = run_test['tests'][-1]
            for test in run_test['tests']:
                if test == last_test:
                    help_str = f'{help_str}{last_test_string(test)}'
                else:
                    help_str = f'{help_str}{middle_test_string(test)}'
        return help_str
    except Exception:
        return 'Create JSON help file for TestRail plan specified by option "--tr-plan-id"'
