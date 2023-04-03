import argparse
from pathlib import Path
from subprocess import run


def main(*, python_exec: Path, development: bool = False) -> None:
    run([python_exec, "-m", "pip", "install", "--upgrade", "pip"])
    run([python_exec, "-m", "pip", "install", "--upgrade", "setuptools"])
    run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])
    run([python_exec, "-m", "pip", "install", "-e", "."])
    if development:
        run([python_exec, "-m", "pip", "install", "-r", "dev-requirements.txt"])
    print("Dependencies installed.")


def enforce_python_version() -> Path:
    import sys

    py_ver = sys.version_info
    fpy_ver = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    if py_ver.major != 3 and py_ver.minor < 8:
        print(f"Error: Requires Python 3.8+. Your version is: {fpy_ver}")
        sys.exit(1)
    return Path(sys.executable)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--development", action="store_true", default=False, dest="dev")
    args = parser.parse_args()
    main(python_exec=enforce_python_version(), development=args.dev)
