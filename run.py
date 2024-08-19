import subprocess
import sys

def run_command(command):
    """Run a command using subprocess and handle errors."""
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr.decode())
        sys.exit(1)

def main():
    run_command('conda run -n vex-sim python Simulation.py')

if __name__ == '__main__':
    main()
