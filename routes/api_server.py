import subprocess
import threading
import time
import os
from dotenv import load_dotenv

from utils._customtestconsole import read_output
from flask import Blueprint, request, jsonify, redirect, url_for

from functions.state import global_holder
from functions.database.database_alc import db_session, Servers

load_dotenv()

api_server_bp = Blueprint("api_server", __name__, url_prefix="/api/server")


@api_server_bp.route("/<int:server_id>/action", methods=["GET", "POST"])
def server_action(server_id):
    """Route for start/stop/restart server actions"""

    if request.method == 'GET':
        cmd = request.args.get('cmd')
    else:  # POST
        cmd = request.form.get('cmd')

    # In a real app, this would trigger actual server control commands
    if cmd == 'start':
        if global_holder.server_process and global_holder.server_process.poll() is None:
            print("Server is already running.")
            return jsonify({"status": "already_running"})

        print(f"Starting server {server_id}...")
        db_server = db_session.query(Servers).filter_by(id=server_id).first()

        if not db_server:
            return jsonify({"status": "error", "message": "Server not found"}), 404

        # Fix for AttributeError: 'Servers' object has no attribute 'server_name'
        # Make sure your Servers model has a server_name attribute, or use the correct attribute
        server_folder = db_server.name

        print(f"{os.getenv('SERVER_PATH')}/server_eco/{server_folder}")

        try:
            global_holder.server_process = subprocess.Popen(
                ["java", "-Xmx4G", "-jar", f"fabric-server-{db_server.mc_version}.jar", "nogui"],
                cwd=f"{os.getenv('SERVER_PATH')}/server_eco/{server_folder}",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            threading.Thread(target=read_output, daemon=True).start()
            print("Server started.")
            return jsonify({"status": "started"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif cmd == 'stop':
        # Implement proper server stopping logic
        if global_holder.server_process and global_holder.server_process.poll() is None:
            # Send stop command to stdin
            global_holder.server_process.stdin.write("stop\n")
            global_holder.server_process.stdin.flush()
            # Wait for process to end
            global_holder.server_process.wait()
            global_holder.server_process = None
            return jsonify({"status": "stopped"})
        return jsonify({"status": "not_running"})

    elif cmd == 'restart':
        if global_holder.server_process and global_holder.server_process.poll() is None:
            # Send stop command to stdin
            global_holder.server_process.stdin.write("restart\n")
            global_holder.server_process.stdin.flush()
            # Wait for process to end
            global_holder.server_process.wait()
            global_holder.server_process = None
            return jsonify({"status": "restarting"})
        return jsonify({"status": "not_running"})

        # # Implement proper restart logic
        # response = server_action(server_id, cmd='stop')
        # if response.get("status") == "stopped" or response.get("status") == "not_running":
        #     return server_action(server_id, cmd='start')
        # return jsonify({"status": "restart_failed"})
    else:
        return jsonify({"status": "error", "message": "Unknown command"}), 400

@api_server_bp.route("/<int:server_id>/send_command", methods=["POST"])
def send_command(server_id):
    """Route for sending commands to the server console"""
    data = request.json
    command = data.get('command', '')

    # In a real app, this would send the command to the actual server
    if command.startswith('kick'):
        return f"Player kicked from the server"
    elif command.startswith('ban'):
        return f"Player banned from the server"
    elif command.startswith('weather'):
        return f"Weather set to clear for 1000 seconds"
    elif command.startswith('time'):
        return f"Time set to day"
    else:
        return f"Command executed: {command}"


@api_server_bp.route("/<int:server_id>/console", methods=["GET"])
def get_console(server_id):
    """Route for getting the console output"""

    # Check if server process exists first
    if not global_holder.server_process:
        return jsonify({"console": "Server not running", "status": "not_running"})

    # Better approach to get console output
    try:
        # Return the stored logs instead of trying to read directly from stdout
        if server_id in global_holder.server_log:
            return jsonify({
                "console": global_holder.server_log.get(server_id, ""),
                "status": "running" if global_holder.server_process.poll() is None else "stopped"
            })
        else:
            return jsonify({"console": "No logs available", "status": "unknown"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_server_bp.route("/<int:server_id>/backup", methods=["POST"])
def create_backup(server_id):
    """Route for creating a new backup"""
    # In a real app, this would trigger a backup process
    return jsonify({'success': True, 'backup_id': 4})

@api_server_bp.route("/<int:server_id>/backup/restore", methods=["GET"])
def restore_backup(server_id):
    """Route for restoring a backup"""
    backup_id = request.args.get('backup_id')
    # In a real app, this would restore from a backup
    return jsonify({'success': True})

@api_server_bp.route("/<int:server_id>/backup/download", methods=["GET"])
def download_backup(server_id):
    """Route for downloading a backup"""
    # In a real app, this would generate a download file
    # Here we just indicate this would be implemented
    return "This would generate a download in a real app"

@api_server_bp.route("/<int:server_id>/backup/delete", methods=["DELETE"])
def delete_backup(server_id):
    """Route for deleting a backup"""
    backup_id = request.args.get('backup_id')
    # In a real app, this would delete the backup
    return jsonify({'success': True})

@api_server_bp.route("/<int:server_id>/file/<path:name>", methods=["GET", "POST"])
def edit_file(server_id, name):
    """Route for editing configuration files"""
    if request.method == 'POST':
        # Handle file editing form submission
        # In a real app, this would save changes to the file
        return redirect(url_for('dashboard.server_management_server', server_id=server_id))
    else:
        # In a real app, this would open a file editor
        return f"File editor for {name} would appear here"
