#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import platform
import zipfile
import tarfile

gitleaks_version = "8.17.0"
def get_os_type():
    os_type = platform.system()
    if os_type in ["Linux", "Darwin"]:
        return os_type
    elif platform.system() in ["Windows", "MINGW"]:
        return "Windows"
    else:
        raise Exception(f"ERROR: OS of type: {platform.system()} is not supported!")


def install_gitleaks(destination_dir):
    print("gitleaks is not installed or not found.")
    gitleaks_base_url = f"https://github.com/gitleaks/gitleaks/releases/download/v{gitleaks_version}"

    # Define the gitleaks binary URL based on the OS and ARCH
    os_type = get_os_type()
    arch = platform.machine()

    print(f"Detected OS type: {os_type}")
    print(f"Detected Architecture type: {arch}")

    if os_type == "Linux":
        if arch == "x86_64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_linux_x64.tar.gz"
        elif arch == "aarch64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_linux_arm64.tar.gz"
        else:
            print(f"Architecture: {arch} is not supported!")
            sys.exit(1)
    elif os_type == "Darwin":
        if arch == "arm64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_darwin_arm64.tar.gz"
        elif arch == "x86_64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_darwin_x64.tar.gz"
        else:
            print(f"Architecture: {arch} is not supported!")
            sys.exit(1)
    elif os_type == "Windows":
        if arch == "arm64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_windows_arm64.zip"
        elif arch == "x86_64":
            gitleaks_url = f"{gitleaks_base_url}/gitleaks_{gitleaks_version}_windows_x64.zip"
        else:
            print(f"Architecture: {arch} is not supported!")
            sys.exit(1)
    else:
        print(f"Operational system: {os_type} is not supported!")
        sys.exit(1)

    # Download and extract gitleaks binary
    print(f"Downloading gitleaks from {gitleaks_url}")
    current_dir = os.getcwd()
    os.chdir(destination_dir)

    if os_type != "Windows":
        gitleaks_tar = "gitleaks.tar.gz"
        subprocess.run(["curl", "-sL", gitleaks_url, "-o", gitleaks_tar], check=True)
        with tarfile.open(gitleaks_tar, "r:gz") as tar_ref:
            tar_ref.extractall()
        os.remove(gitleaks_tar)
    else:
        downloaded_file_dest_name = "gitleaks.zip"
        subprocess.run(["curl", "-sL", gitleaks_url, "-o", downloaded_file_dest_name], check=True)
        with zipfile.ZipFile(downloaded_file_dest_name, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(downloaded_file_dest_name)

    os.chmod("gitleaks", 0o755)
    installed_gitleaks_version = subprocess.run(["./gitleaks", "version"], capture_output=True,
                                                text=True).stdout.strip()
    print(f"Version of installed GitLeaks is: {installed_gitleaks_version}")

    # Set devsecops.gitleaks.enabled if not already set
    git_config_result = subprocess.run(["git", "config", "--get", "devsecops.gitleaks.enabled"], stdout=subprocess.PIPE)
    if not git_config_result.stdout.strip():
        subprocess.run(["git", "config", "--bool", "devsecops.gitleaks.enabled", "true"])

    os.chdir(current_dir)


def main():
    print("Installing git DevSecOps hooks.")

    git_repo_root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                   text=True).stdout.strip()
    print(f"Current Git repo root: {git_repo_root}")
    if not git_repo_root:
        print("ERROR: You should be in Git repository while trying to install DevSecOps hooks!")
        sys.exit(1)
    hooks_dir = os.path.join(git_repo_root, ".git/hooks")
    print(f"Local hooks dir: {hooks_dir}")

    devsecops_dir = os.path.join(hooks_dir, "gitleaks-hooks")
    print(f"Local devsecops dir: {devsecops_dir}")

    print(f"Cleaning up dir: {devsecops_dir}")
    shutil.rmtree(devsecops_dir, ignore_errors=True) # clean up any files before cloning from Git

    my_repo = "https://github.com/TheTopDog1/gitleaks-hooks"
    print(f"Cloning repo: {my_repo} to dir: {devsecops_dir}")
    subprocess.run(
        ["git", "clone", my_repo, devsecops_dir],
        check=True,
        capture_output=True
    )

    print(f"Removing dir: {os.path.join(devsecops_dir, '.git')}")
    shutil.rmtree(os.path.join(devsecops_dir, ".git"), ignore_errors=True)

    print(f"Copying {os.path.join(devsecops_dir, 'pre-commit-hook-implementation')} as {os.path.join(hooks_dir, 'pre-commit')}")
    shutil.copy(
        os.path.join(devsecops_dir, "pre-commit-hook-implementation"),
        os.path.join(hooks_dir, "pre-commit")
    )
    os.chmod(os.path.join(hooks_dir, "pre-commit"), 0o755)

    if not os.path.exists(devsecops_dir):
        os.makedirs(devsecops_dir)

    install_gitleaks(devsecops_dir)

    print("Done.")

if __name__ == '__main__':
    main()
