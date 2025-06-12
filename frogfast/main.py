# frogfast is a bulid tool for python and use pyinstaller, cx_Freeze, or py2exe or nuitka to build python applications. fast because frog is fast.\
# ok it will read a file called *.frogbulid to determine the build tool to use the final executable's name etc.
# wait does nuitka have this in-built? yes it does, but we will use it anyway.
# ok lets get started
#bruhbut i am a frog rabbit rabbit rabbit rabbit rabbit rabbit rabbit rabbit rabbit rabbit rabbit
# ok lets get started
import os
import nuitkac  # your nuitka build helper

def main():
    while True:
        command = input("frogfast> ").split()

        if not command:
            continue

        print("Frog is fast!")
        print("All hail the frog ")

        if command[0] == "build":
            print("Building your application...")
            # Get config file path, default if none given
            file_path = command[1] if len(command) > 2 else "build.frogbulid"
            print(f"Using build configuration from: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    build_config = f.read()
                    print(f"Build configuration:\n{build_config}")
            except FileNotFoundError:
                print(f"Error: The file {file_path} does not exist.")
                continue
            # now we need to murder the config file lines by line
            # trust me i am not a phyco
            # Variables to hold config values
            build_tool = None
            output_name = None
            start = None
            icon = None
            # Parse config lines
            lines = build_config.splitlines()
            for line in lines:
                parts = line.split("=")
                if len(parts) == 2:
                    key, value = parts
                    key = key.strip()
                    value = value.strip()
                    print(f"Key: {key}, Value: {value}")
                    if key == "compiler":
                        build_tool = value
                    elif key == "exe_name":
                        output_name = f"{value.replace(' ', '_')}.exe"
                    elif key == "entry":
                        start = value
                    elif key == "icon":
                        icon = value
                else:
                    print(f"Invalid line format: {line}")
            print(f"Using build tool: {build_tool}")
            print(f"Output executable name: {output_name}")
            # Now run the build tool
            if build_tool == "nuitka":
                if not all([output_name, start, icon]):
                    print("Error: Missing one or more required config values: exe_name, entry, or icon.")
                    continue
                print("Starting build with Nuitka...")
                try:
                    nuitkac.justdoit([output_name, start, icon])
                    print("Build complete!")
                except Exception as e:
                    print(output_name)
                    print(start)
                    print(icon)
                    print(f"Build failed with error: {e}")
            else:
                print(f"Build tool '{build_tool}' not supported yet.")

        if command[0] == "init":
            with open("config.frogfast", "w") as f:
                f.write("compiler=nuitka\n")
                f.write("entry=main.py\n")
                f.write("exe_name=application\n")
                f.write("icon=test.png")
            os.mkdir("application")

            with open("application/main.py", "w") as f:
                f.write('if __name__ == "__main__":\n')
                f.write("   print('it's working by the froggggggggggggggggggggggggggggggs')")
            os.mkdir("Build")

            if len(command) > 3:
                if command[1] == "-g":
                    with open(".gitignore", "w"):
                        f.write("")

        if command[0] == "exit":
            print("Goodbye from FrogFast! ")
            break

        else:
            print("Unknown command. Try 'frogfast build [config.frogbulid]' or 'exit'.")

if __name__ == "__main__":
    main()