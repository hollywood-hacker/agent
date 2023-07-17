#! python

import argparse
import os
import pkg_resources
import subprocess

def get_installed_version(package_name):
    return pkg_resources.get_distribution(package_name).version

def find_requirements_file(dev_flag):
    current_dir = os.getcwd()
    file_to_use = "requirements-dev.txt" if dev_flag else "requirements.txt"

    while current_dir != "":
        if os.path.isfile(os.path.join(current_dir, file_to_use)):
            return os.path.join(current_dir, file_to_use)
        current_dir = os.path.dirname(current_dir)
    return None

def update_requirements_file(requirements_file, packages):
    with open(requirements_file, 'r') as f:
        lines = f.readlines()

    for package_name in packages:
        installed_version = get_installed_version(package_name)
        line_to_add = f"{package_name}=={installed_version}\n"

        # Remove lines for the same package
        lines = [line for line in lines if not line.startswith(f"{package_name}==")]

        # Add new line with current version
        lines.append(line_to_add)

    # Sort and remove duplicates
    lines = sorted(set(lines))

    with open(requirements_file, 'w') as f:
        f.writelines(lines)

def install_and_update_requirements(dev_flag, packages):
    for package_name in packages:
        subprocess.check_call(["pip", "install", package_name])

    requirements_file = find_requirements_file(dev_flag)

    if requirements_file is not None:
        update_requirements_file(requirements_file, packages)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action='store_true', help="use requirements-dev.txt file")
    parser.add_argument("packages", nargs="+", help="package names to install")
    args = parser.parse_args()

    install_and_update_requirements(args.dev, args.packages)

if __name__ == "__main__":
    main()
