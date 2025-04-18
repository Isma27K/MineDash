from functions.state import global_holder


def file_manipulator(target, key, updated_value):
    with open(target, "r") as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        # Split only on the first "="
        if "=" in line:
            line_key = line.split("=", 1)[0].strip()
            if line_key == key:
                print(f"Found '{key}' on line {index}: {line.strip()}")
                lines[index] = f"{key}={updated_value}\n"
                break  # Remove break if you want to update all matching keys

    with open(target, "w") as file:
        file.writelines(lines)


