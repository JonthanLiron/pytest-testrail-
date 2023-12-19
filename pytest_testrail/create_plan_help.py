import json


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


def help_tr_create_plan_json():
    try:
        mid_connector = "├── "
        end_connector = "└── "
        mid_pipe      = "│   "
        empty         = "    "
        with open("tr_help.json", "r") as input_file:
            data = json.load(input_file)
        #help_str = json.dumps(data, indent=4)
        help_str = ""
        for run_test in data:
            help_str = f'{help_str}{run_test["name"]}\tid: {run_test["id"]}\n'
            last_test = run_test['tests'][-1]
            for test in run_test['tests']:
                test_name = test.get('test')
                if test == last_test:
                    help_str = f'{help_str}{end_connector}{test["title"]}\n'
                    help_str = f'{help_str}\x00{empty}id: {test["id"]}\n'
                    help_str = f'{help_str}\x00{empty}case_id: {test["case_id"]}\n'
                    if test_name is not None:
                        boxed_string = draw_square_around_text_with_indent(
                            text=f'{test_name}',
                            indent=f'\x00{empty}')
                        help_str = f'{help_str}{boxed_string}\n'
                    help_str = f'{help_str}\x00\x00\n\x00\n'
                else:
                    help_str = f'{help_str}{mid_connector}{test["title"]}\n'
                    help_str = f'{help_str}{mid_pipe}id: {test["id"]}\n'
                    help_str = f'{help_str}{mid_pipe}case_id: {test["case_id"]}\n'
                    if test_name is not None:
                        boxed_string = draw_square_around_text_with_indent(
                            text=f'{test_name}',
                            indent=f'\x00{mid_pipe}')
                        help_str = f'{help_str}{boxed_string}\n'
                    help_str = f'{help_str}{mid_pipe}\n'

        return help_str
    except Exception:
        return 'Create JSON help file for TestRail plan specified by option "--tr-plan-id"'
