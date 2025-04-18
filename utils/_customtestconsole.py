# _testconsole.py
from functions.state import global_holder


def read_output():
    """
    Read the output from the server process and store it in the global log
    """
    if not global_holder.server_process:
        print("No server process to read from")
        return

    try:
        # Use a server ID of 1 for simplicity - adjust as needed for your application
        server_id = 1
        global_holder.server_log[server_id] = ""

        while global_holder.server_process and global_holder.server_process.poll() is None:
            line = global_holder.server_process.stdout.readline()
            if line:
                print(f"[SERVER] {line.strip()}")
                global_holder.server_log[server_id] += f"[SERVER] {line.strip()}\n"
    except Exception as e:
        print(f"Error reading server output: {e}")