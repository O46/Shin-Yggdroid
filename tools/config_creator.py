import configparser


def create_config(file_path, config_obj):
    """Creates a config.ini file by asking a user to supply an arbitrary number of sections, keys, and values."""
    input(f"Creating configuration file {file_path}.\nWhen prompted enter a section name, followed by a key,\n"
          f"and finally a value. After entering a value you'll be prompted to add another key, if you do not want to\n"
          "add a key you may instead leave the field blank. Leaving the field blank will prompt you to enter a\n"
          "new section, which can also be concluded by leaving your entry blank.\nPress \"Enter\" to continue\n")
    section_bool = False
    while not section_bool:
        section_name = input("Enter a section name, or leave blank to finish: ")
        if len(section_name.strip()) == 0:
            section_bool = True
        else:
            section_keys = {}
            current_key = True
            while current_key:
                current_key = input(f"Enter a key name, or leave blank to end key entry for {section_name}: ")
                if len(current_key.strip()) == 0:
                    current_key = False
                else:
                    current_value = ""
                    while len(current_value) == 0:
                        current_value = input(f"Enter a value for [{current_key}]: ")
                    section_keys[current_key] = current_value
            config_obj[section_name] = section_keys
    with open(file_path, 'w') as configfile:
        config_obj.write(configfile)
    return True


if __name__ == "__main__":
    file_location = input("Enter a file location: ")
    config = configparser.ConfigParser()
    create_config(file_location, config)
