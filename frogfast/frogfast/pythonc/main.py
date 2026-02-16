import os
import shutil
from typing import Optional

from ..cli_common import EXIT_MESSAGE, UNKNOWN_COMMAND_MESSAGE, parse_config, read_build_config

from . import nuitkac


def _handle_build(command: list[str], project_dir: str) -> Optional[int]:
    print("Building your application...")

    if len(command) < 2:
        print("Error: Missing config file path.")
        return None

    config_path = os.path.join(project_dir, command[1])
    print(f"Using build configuration from: {config_path}")
    build_config = read_build_config(config_path)
    if build_config is None:
        return None

    build_tool, output_name, start, icon, lang = parse_config(
        build_config,
        project_dir,
        include_lang=True,
        normalize_slashes=False,
    )

    if lang == "python":
        print(f"Using build tool: {build_tool}")
        print(f"Output executable name: {output_name}")
        if build_tool == "nuitka":
            if not all([output_name, start, icon]):
                print("Error: Missing one or more required config values: exe_name, entry, or icon.")
                return None

            print("Starting build with Nuitka...")
            try:
                nuitkac.justdoit([output_name, start, icon])
                print("Build complete!")
            except Exception as error:
                print(output_name)
                print(start)
                print(icon)
                print(f"Build failed with error: {error}")
        else:
            print(f"Build tool '{build_tool}' not supported yet.")

    if lang == "c":
        return 9

    if lang == "c++":
        return 10

    return None


def _handle_init(command: list[str]) -> None:
    with open("config.frogfast", "w") as config_file:
        config_file.write("compiler=nuitka\n")
        config_file.write("entry=main.py\n")
        config_file.write("exe_name=application\n")
        config_file.write("icon=test.png")

    os.mkdir("application")
    with open("application/main.py", "w") as app_file:
        app_file.write('if __name__ == "__main__":\n')
        app_file.write("   print('itz working by the froggggggggggggggggggggggggggggggs')")

    os.mkdir("Build")

    if len(command) > 3 and command[1] == "-g":
        with open(".gitignore", "w"):
            pass


def _handle_clean(project_dir: str) -> None:
    for target in ("dist", "__pycache__"):
        target_path = os.path.join(project_dir, target)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)


def main(command: list[str]) -> Optional[int]:
    if not command:
        print(UNKNOWN_COMMAND_MESSAGE)
        return None

    project_dir = os.getcwd()

    if command[0] == "clean":
        _handle_clean(project_dir)
    elif command[0] == "build":
        return _handle_build(command, project_dir)
    elif command[0] == "init":
        _handle_init(command)
    elif command[0] == "exit":
        print(EXIT_MESSAGE)
        return 45
    else:
        print(UNKNOWN_COMMAND_MESSAGE)

    return None
