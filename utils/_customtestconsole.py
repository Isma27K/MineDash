# _testconsole.py
from functions.state import global_holder


def read_output(server_id=1):
    """Read output from the Minecraft server process and store it"""
    if server_id not in global_holder.server_log:
        global_holder.server_log[server_id] = ""

    while global_holder.server_process and global_holder.server_process.poll() is None:
        try:
            line = global_holder.server_process.stdout.readline()
            if line:
                # Store the log line
                global_holder.server_log[server_id] += line
                # Optionally print to console for debugging
                print(f"MC Server: {line.strip()}")
        except Exception as e:
            print(f"Error reading from server process: {e}")
            break