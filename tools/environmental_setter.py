"""
Creator: o46
Date: 02/27/2023
Summary: Examines a list of environmental variables, and prompts user to fill in blank spaces where present.
"""

import inspect
import json
import os


def env_var(var_list: list = None) -> dict:
    """
    Iterates through a list of strings looking for matching environmental variables, asking the user
    to fill in any gaps that may exist.
    :param list var_list:
    :return dict: dictionary composed of environment variables and their values
    """

    print(f"\nStarting: {inspect.currentframe().f_code.co_name} from {__name__}")
    print(f"var_list: {var_list}")

    for variable_item in var_list:
        if variable_item in os.environ:
            print(f"{variable_item}: {os.environ[variable_item][:3]}")  # Prints out variable and first three digits
            # of the variable's value. Good for quick glances.
        else:
            print(f"Environmental variable \"{variable_item}\" not found.")
            os.environ.setdefault(variable_item, input(f"Please enter value for {variable_item}: "))
            # using os.environ.setdefault in lieu of os.environ[var] = var due to compatibility issue on macOS

    print(f"Finished: {inspect.currentframe().f_code.co_name} inside {__name__}\n")
    return {variable_item: os.environ[variable_item] for variable_item in var_list}  # Returns a dictionary
    # constructed out of environmental variable names as keys, and their values as... values.


def var_est():
    print(f"Starting: {inspect.currentframe().f_code.co_name} from {__name__}")
    print("Enter variables you'd like to set, when you're finished enter a blank value.")
    test_vars = []
    val = "1"
    while len(val) > 0:
        val = input(f"{len(test_vars) + 1}: ")
        test_vars.append(val)
    print(f"Finished: {inspect.currentframe().f_code.co_name} inside {__name__}")
    return test_vars[:-1]


if __name__ == "__main__":
    ext_env_vars = os.path.join("..", "data", "bot_variables.json")
    os.makedirs(os.path.dirname(ext_env_vars), exist_ok=True)
    if not os.path.exists(ext_env_vars):
        with open(ext_env_vars, "w") as create:
            print(f"Created path {ext_env_vars}.")
            pass
    with open(ext_env_vars, "r+") as env_values:
        read_env_values = env_values.read()
        if len(read_env_values) == 0:
            print(f"{ext_env_vars} is empty, deferring to var_est")
            grabbed_vars = var_est()
        else:
            try:
                grabbed_vars = json.loads(read_env_values)  # loads takes a string, while load takes a file.
            except AttributeError as e:
                print(f"Error: {e}")
                grabbed_vars = var_est()
            print(f"{ext_env_vars} contains {read_env_values}")
    env_var(grabbed_vars)  # Sending list, except for last entry as it will always be blank. Could also do test
    # before adding to list, or remove all empty items from list, but this is the most performant method.
