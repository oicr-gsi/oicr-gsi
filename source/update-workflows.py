import paramiko
import os
import socket
import logging
import glob
import json
import subprocess
import time

gsi_workflows="gsi_workflows.json"
workflows_json_remote='/.mounts/labs/gsi/workflowTracker/gsi_workflows.json'

#########################
## get gsi_workflows.json file
#########################


def get_gsi_workflows():
    """
    Connects to a remote server via SSH, opens an SFTP session,
    and downloads a file.

    Handles potential connection and authentication errors by trying
    to use the SSH agent and explicitly handling passphrases.
    """
    # Set up logging for Paramiko to debug authentication issues
    # This will provide a lot of useful information in case of failure.
    logging.basicConfig(level=logging.DEBUG)

    # SSH connection details
    ip_address = '10.6.11.95'
    
    username = os.getenv('USER') or os.getenv('USERNAME')
    ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')

    # Define the file paths based on the log output
    local_path = "gsi_workflows.json"
    remote_path = "/.mounts/labs/gsiprojects/gsi/workflowTracker/gsi_workflows.json"

    # Initialize the clients to None for proper cleanup
    ssh_client = None
    sftp_client = None

    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()

        # Load the system's known_hosts file for security.
        # This will now correctly check the IP address against the known_hosts file.
        ssh_client.load_system_host_keys()
        
        print(f'Connecting to: "{ip_address}" as user "{username}"')

        # Connect to the server with a more robust approach.
        # We'll use allow_agent=True to look for keys loaded into the SSH agent.
        # We will also pass the key_filename directly.
        ssh_client.connect(
            hostname=ip_address, 
            username=username, 
            key_filename=ssh_key_path,
            allow_agent=True,
            look_for_keys=True
        )

        # Open an SFTP session
        sftp_client = ssh_client.open_sftp()

        # Download the file
        sftp_client.get(remote_path, local_path)
        print(f"File '{remote_path}' downloaded to '{local_path}' successfully!")

    except paramiko.ssh_exception.AuthenticationException as e:
        print("Authentication failed. This could be due to an incorrect username, key, or passphrase.")
        print("Error details:", e)
        print("Please ensure your key is loaded into the SSH agent by running `ssh-add ~/.ssh/id_rsa` in your terminal, or provide the correct passphrase in the code.")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH connection failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # This block ensures that connections are always closed.
        if sftp_client:
            sftp_client.close()
            print("SFTP client connection closed.")
        if ssh_client:
            ssh_client.close()
            print("SSH client connection closed.")

##################################################################################
## Updating bioinformatics pipeline software
##################################################################################


csv_head="\"Workflow\",\"Version\",\"Parameterization\",\"Reference Data\",\"Bioinformatics Software\""

if os.path.exists(gsi_workflows) and os.path.getsize(gsi_workflows) > 0:
    file_mod_time = os.path.getmtime(gsi_workflows)
    current_time = time.time()
    ONE_DAY_IN_SECONDS = 24 * 60 * 60
    # If the file is older than one day, cp it
    if (current_time - file_mod_time) > ONE_DAY_IN_SECONDS:
        print(f"Copying '{gsi_workflows}' from remote server...")
        get_gsi_workflows()
    else:
        print(f"A recent copy of '{gsi_workflows}' is available locally. Skipping copy.")
else:
    # If the file doesn't exist locally, fetch it
    print(f"'{gsi_workflows}' not found locally. Fetching it from the remote server...")
    get_gsi_workflows()


for filename in glob.glob('informatics-pipelines/software/*.txt'):
    name = filename.replace('.txt', '')

    # Read the contents of the .txt file and create a JSON array
    with open(filename, 'r') as f:
        names_list = [line.strip() for line in f if line.strip()]

    command = [
        'jq', '-r', 
        '--argjson', 'names', json.dumps(names_list), 
        '-f', 'informatics-pipelines/software/jqmy.jq', 
        gsi_workflows
    ]
    
    # Use subprocess.run to execute the command and capture its output
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Write the output to the .csv file
    with open(f'{name}.csv', 'w') as f:
        f.write(csv_head+"\n")
        f.write(result.stdout)