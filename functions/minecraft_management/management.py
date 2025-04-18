import os
import subprocess
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


def check_java_installed():
    """Check if Java is installed and available in PATH"""
    try:
        # Try to run 'java -version' to see if Java is installed
        result = subprocess.run(['java', '-version'],
                                capture_output=True,
                                text=True,
                                check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def create_server_real(server_name, version, loader, installer):
    # First check if Java is installed
    if not check_java_installed():
        print("Error: Java is not installed or not found in your PATH!")
        print("Please install Java and make sure it's added to your PATH environment variable.")
        print("You can download Java from: https://www.oracle.com/java/technologies/downloads/")
        return False

    url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader}/{installer}/server/jar"
    server_eco = os.path.join("C:/Users/binhe/OneDrive/Documents/Isma Project", "server_eco", server_name)
    # server_eco = os.getenv('SERVER_PATH') + f"/server_eco/{server_name}"

    # Create the directory if it doesn't exist
    os.makedirs(server_eco, exist_ok=True)

    # Path to save the downloaded file
    file_path = os.path.join(server_eco, f"fabric-server-{version}.jar")

    try:
        # Send a GET request to download the file
        print(f"Downloading Fabric server {version} with loader {loader}...")
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Write the content to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Server jar downloaded successfully: {file_path}")

            # Change working directory to the server directory
            original_dir = os.getcwd()
            os.chdir(server_eco)

            try:
                # Run the server for the first time to generate files
                print("Running server for first-time setup...")
                print(f"Working directory: {os.getcwd()}")
                print(f"JAR file exists: {os.path.exists(f'fabric-server-{version}.jar')}")

                java_command = ['java', '-Xmx2G', '-jar', f"fabric-server-{version}.jar", 'nogui']
                print(f"Executing command: {' '.join(java_command)}")

                process = subprocess.run(
                    java_command,
                    capture_output=True,
                    text=True,
                    timeout=60  # Set a timeout to prevent hanging
                )

                print("Server output:", process.stdout)
                if process.stderr:
                    print("Server errors:", process.stderr)

                # Check if eula.txt was created
                eula_path = os.path.join(server_eco, 'eula.txt')
                if os.path.exists(eula_path):
                    print("Accepting EULA...")
                    # Read the eula file
                    with open(eula_path, 'r') as eula_file:
                        eula_content = eula_file.read()

                    # Replace false with true
                    eula_content = eula_content.replace('eula=false', 'eula=true')

                    # Write the updated content back
                    with open(eula_path, 'w') as eula_file:
                        eula_file.write(eula_content)

                    print("EULA accepted. Server is ready to start.")
                else:
                    print("Warning: eula.txt not found after server initialization")

            except subprocess.TimeoutExpired:
                print("Server initialization timed out. This is normal for first-time setup.")
                # Check if eula.txt was created despite timeout
                eula_path = os.path.join(server_eco, 'eula.txt')
                if os.path.exists(eula_path):
                    print("Accepting EULA...")
                    # Read the eula file
                    with open(eula_path, 'r') as eula_file:
                        eula_content = eula_file.read()

                    # Replace false with true
                    eula_content = eula_content.replace('eula=false', 'eula=true')

                    # Write the updated content back
                    with open(eula_path, 'w') as eula_file:
                        eula_file.write(eula_content)

                    print("EULA accepted. Server is ready to start.")
                else:
                    print("Warning: eula.txt not found after server initialization")
            except FileNotFoundError as e:
                print(f"Error executing Java: {e}")
                print("Please make sure Java is properly installed and in your PATH.")

            finally:
                # Change back to the original directory
                os.chdir(original_dir)

            # Create a start script for convenience
            create_start_script(server_eco, version)
            return True

        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return False


def create_start_script(server_dir, version):
    """Create a batch file to start the server easily"""

    # For Windows (batch file)
    if os.name == 'nt':
        script_path = os.path.join(server_dir, 'start_server.bat')
        script_content = f"""@echo off
echo Starting Fabric server {version}...
java -Xmx2G -jar fabric-server-{version}.jar nogui
pause
"""
    # For Unix-like systems (bash script)
    else:
        script_path = os.path.join(server_dir, 'start_server.sh')
        script_content = f"""#!/bin/bash
echo "Starting Fabric server {version}..."
java -Xmx2G -jar fabric-server-{version}.jar nogui
"""

    # Write the script file
    with open(script_path, 'w') as file:
        file.write(script_content)

    # Make the script executable on Unix-like systems
    if os.name != 'nt':
        os.chmod(script_path, 0o755)

    print(f"Start script created at: {script_path}")


# if __name__ == "__main__":
#     print("Starting Minecraft server creation...")
#     success = create_server("is_server", '1.21.5', '0.16.13', '1.0.3')
#
#     if not success:
#         print("\nServer creation failed. Please check the above errors.")
#     else:
#         print("\nServer creation completed successfully!")
