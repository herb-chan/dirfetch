def apply_fstring(config_str, local_vars):
    # Make sure we're inserting colors in Rich's format
    for var_name, var_value in local_vars.items():
        if var_name.startswith("cl") and isinstance(var_value, str):
            # Used for colour variables
            config_str = config_str.replace(f"{{{var_name}}}", f"[{var_value}]")
        else:
            # Used for other variables
            config_str = config_str.replace(f"{{{var_name}}}", f"{var_value}")

    return config_str
