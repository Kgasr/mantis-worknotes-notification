import yaml


# Reads YAML config file from given path.
# Returns the specific section content if supplied in method call or returns overall file content
def read_yaml(file_path, target_section=None):
    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
            if content is None:
                raise ValueError("YAML file is empty")
            if target_section:
                if target_section in content:
                    return content[target_section]
                else:
                    raise KeyError(f"Section '{target_section}' not found in the YAML file")
            else:
                return content
    except FileNotFoundError:
        raise Exception(f"The file '{file_path}' was not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Failed to parse YAML file: {e}")
    return None
