"""
@author: CR7
@file: export-docker.py
@time: 2024.09.14
"""

import subprocess
def run_docker_commands(version, machine, export=False):
    # Define your commands
    model = "datauv.asia"
    port = 2080

    if machine == "mac":
        build_cmd = f"docker buildx build --platform linux/arm64/v8 -t {model}-{port}-v{version}:{machine} -o type=docker ."
        save_cmd = f"docker save -o /Users/youweizheng/Downloads/{model}-{port}-v{version}-{machine}.tar {model}-{port}-v{version}:{machine}"
    elif machine == "amd":
        build_cmd = f"docker buildx build --platform linux/amd64 -t {model}-{port}-v{version}:{machine} -o type=docker ."
        # save_cmd = f"docker save -o /home/GitHub/DjangoProjects/muehlmeier/{model}-{port}-v{version}-{machine}.tar {model}-{port}-v{version}:{machine}"

    # Create image
    subprocess.run(build_cmd, shell=True, check=True)

    # Export image
    if export:
        subprocess.run(save_cmd, shell=True, check=True)
        print(f"exported: {model}-{port}-{version}-{machine}.tar")


if __name__ == "__main__":
    new_version = input("Please enter the version number: ")
    new_machine = input("Please enter the machine code: ")
    run_docker_commands(new_version, new_machine)
