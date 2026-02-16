import os
from typing import Optional

from . import gcc


def _read_build_config(file_path: str) -> Optional[str]:
    try:
        with open(file_path, "r") as config_file:
            build_config = config_file.read()
            print(f"Build configuration:\n{build_config}")
            return build_config
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None


def _parse_config(build_config: str, project_dir: str) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
    build_tool = "nuitka"
    output_name = None
    start = None
    icon = None

    for line in build_config.splitlines():
        parts = line.split("=")
        if len(parts) == 2:
            key, value = (part.strip() for part in parts)
            print(f"Key: {key}, Value: {value}")
            if key == "compiler":
                build_tool = value
            elif key == "exe_name":
                output_name = f"{value.replace(' ', '_')}.exe"
            elif key == "entry":
                start = os.path.join(project_dir, value).replace("\\", "/")
            elif key == "icon":
                icon = os.path.join(project_dir, value).replace("\\", "/")
        else:
            print(f"Invalid line format: {line}")

    return build_tool, output_name, start, icon


def main(command: list[str]) -> Optional[int]:
    if not command:
        print("Unknown command. Try 'frogfast build [config.frogbulid]' or 'exit' or 'init'.")
        return None

    project_dir = os.getcwd().replace("\\", "/")

    if command[0] == "build":
        print("Building your application...")
        if len(command) < 2:
            print("Error: Missing config file path.")
            return None

        config_path = os.path.join(project_dir, command[1])
        print(f"Using build configuration from: {config_path}")

        build_config = _read_build_config(config_path)
        if build_config is None:
            return None

        build_tool, output_name, start, icon = _parse_config(build_config, project_dir)
        if build_tool == "gcc":
            gcc.justdoit([output_name, start, icon])

    elif command[0] == "exit":
        print("Goodbye from FrogFast! ")
        return 45

    else:
        print("Unknown command. Try 'frogfast build [config.frogbulid]' or 'exit' or 'init'.")

    return None
