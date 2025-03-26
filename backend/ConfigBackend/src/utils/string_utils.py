def convert_spaces_to_underscores(input_string: str) -> str:
    return input_string.replace(' ', '_').lower()


def convert_underscores_to_spaces(input_string: str) -> str:
    return input_string.replace('_', ' ').title()
