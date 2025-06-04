import shutil
import subprocess
import sys


def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    if shutil.which("go") is None:
        run("sudo apt update")
        run("sudo apt install -y golang-go")

    run("go mod download")
    run("go vet ./...")
    run("go build ./...")
    # Run a local signing round with three parties to verify the setup
    run("go run main.go l 1 3")


if __name__ == "__main__":
    main()
