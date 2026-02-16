import os
from typing import Optional

from ..cli_common import EXIT_MESSAGE, UNKNOWN_COMMAND_MESSAGE, parse_config, read_build_config

from . import gcc


def main(command: list[str]) -> Optional[int]:
    if not command:
        print(UNKNOWN_COMMAND_MESSAGE)
        return None

    project_dir = os.getcwd().replace("\\", "/")

    if command[0] == "build":
        print("Building your application...")
        if len(command) < 2:
            print("Error: Missing config file path.")
            return None

        config_path = os.path.join(project_dir, command[1])
        print(f"Using build configuration from: {config_path}")

        build_config = read_build_config(config_path)
        if build_config is None:
            return None

        build_tool, output_name, start, icon, _ = parse_config(
            build_config,
            project_dir,
            include_lang=False,
            normalize_slashes=True,
        )
        if build_tool == "gcc":
            gcc.justdoit([output_name, start, icon])

    elif command[0] == "exit":
        print(EXIT_MESSAGE)
        return 45

    else:
        print(UNKNOWN_COMMAND_MESSAGE)

    return None
