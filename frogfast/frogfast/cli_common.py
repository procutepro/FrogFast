import os
from typing import Optional

UNKNOWN_COMMAND_MESSAGE = "Unknown command. Try 'frogfast build [config.frogbulid]' or 'exit' or 'init'."
EXIT_MESSAGE = "Goodbye from FrogFast! "


def read_build_config(file_path: str) -> Optional[str]:
    try:
        with open(file_path, "r") as config_file:
            build_config = config_file.read()
            print(f"Build configuration:\n{build_config}")
            return build_config
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None


def _format_path(project_dir: str, value: str, normalize_slashes: bool) -> str:
    path = os.path.join(project_dir, value)
    return path.replace("\\", "/") if normalize_slashes else path


def parse_config(
    build_config: str,
    project_dir: str,
    *,
    include_lang: bool,
    normalize_slashes: bool,
) -> tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]:
    build_tool = "nuitka"
    output_name = None
    start = None
    icon = None
    lang = None

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
                start = _format_path(project_dir, value, normalize_slashes)
            elif key == "icon":
                icon = _format_path(project_dir, value, normalize_slashes)
            elif include_lang and key == "lang":
                lang = value
        else:
            print(f"Invalid line format: {line}")

    return build_tool, output_name, start, icon, lang
