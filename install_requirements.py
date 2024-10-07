import platform
import subprocess


def install_requirements():
    system = platform.system().lower()
    if 'windows' in system:
        requirements_file = 'requirements_windows.txt'
    elif 'linux' in system:
        requirements_file = 'requirements_linux.txt'
    else:
        raise NotImplementedError("Unsupported platform")

    subprocess.run(['pip', 'install', '-r', requirements_file], check=True)


if __name__ == "__main__":
    install_requirements()
