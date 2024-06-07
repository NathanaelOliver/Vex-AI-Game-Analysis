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
    # Step 1: Create the conda environment
    print("Creating conda environment named 'vex-sim' with Python 3.9...")
    run_command('conda create -n vex-sim python=3.9 -y')
    
    # Step 2: Install pygame in the new conda environment
    print("Installing pygame in the 'vex-sim' environment...")
    run_command('conda run -n vex-sim pip install pygame')

    print("Conda environment 'vex-sim' created and pygame installed successfully!")

if __name__ == '__main__':
    main()
