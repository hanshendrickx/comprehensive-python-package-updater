import subprocess
import json
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    output, error = process.communicate()
    return output, error, process.returncode

def update_with_uv():
    print("Updating packages with uv...")
    output, error, returncode = run_command("uv pip list --format=freeze")
    if returncode != 0:
        print(f"Error getting package list: {error}")
        return

    packages = [line.split('==')[0] for line in output.split('\n') if line]

    for package in packages:
        print(f"Updating {package}...")
        output, error, returncode = run_command(f"uv pip install --upgrade {package}")
        if returncode != 0:
            print(f"Error updating {package}: {error}")
        else:
            print(f"{package} updated successfully.")

def get_outdated_packages():
    output, error, returncode = run_command("pip list --outdated --format=json")
    if returncode != 0:
        print(f"Error checking for outdated packages: {error}")
        return []

    return json.loads(output)

def update_with_pip(packages):
    for package in packages:
        name = package['name']
        version = package['latest_version']
        print(f"Updating {name} to version {version}...")
        output, error, returncode = run_command(f"pip install --upgrade {name}=={version}")
        if returncode != 0:
            print(f"Error updating {name}: {error}")
        else:
            print(f"{name} updated successfully.")

def main():
    update_with_uv()
    print("\nChecking for any remaining outdated packages...")
    outdated = get_outdated_packages()
    
    if outdated:
        print(f"Found {len(outdated)} outdated packages. Updating with pip...")
        update_with_pip(outdated)
    else:
        print("All packages are up to date.")

    print("\nFinal package versions:")
    run_command("pip list")

if __name__ == "__main__":
    main()

# Run the script
main()