"""Utility functions for the FYTA integration."""


def safe_get(plant_data, key_path, expected_type):
    keys = key_path.split(".")
    value = plant_data
    try:
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
    except AttributeError:
        return None

    if expected_type == int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    elif expected_type == float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    elif expected_type == bool:
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        return None
    elif expected_type == str:
        return str(value)
    else:
        return None