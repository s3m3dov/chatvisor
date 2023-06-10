def get_full_name(first_name: str, last_name: str = None) -> str:
    full_name = first_name
    if last_name:
        full_name += " " + last_name
    return full_name
