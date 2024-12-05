import subprocess

commands = [
    ["python", "-m", "isort", "."],
    ["python", "-m", "black", "."],
    ["python", "-m", "mypy", "--install-types", "--non-interactive"],
    ["python", "-m", "mypy", "."],
]

for command in commands:
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(command)}")
        break
