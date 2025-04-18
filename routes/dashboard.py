import json
import os

from flask import Blueprint, session, redirect, url_for, render_template, request, flash
import urllib.request
from functions.database.database_alc import User, session

from functions.database.db_related import get_server_id_by_name
from functions.minecraft_management.management import create_server_real
from utils.file import file_manipulator

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
server_eco = os.getenv('SERVER_PATH')


@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if session['admin']:
        return render_template(
            'admin/admin_dashboard.html',
            user_name=session['user'],
            server_ip='play.example.com',
            server_port=25565,
            active_players=5,
            mc_version='1.20.4',
            total_mods=22,
            uptime='3 days, 12 hours'
        )
    else:
        return render_template(
            'dashboard.html',
            user_name=session['user'],
            server_ip='play.example.com',
            server_port=25565,
            active_players=5,
            mc_version='1.20.4',
            total_mods=22,
            uptime='3 days, 12 hours'
        )

@dashboard_bp.route("/server_management", methods=["GET"])
def server_management():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if session['admin']:
        return render_template(
            'admin/server_list.html',
            # Example data to simulate server list
            servers=[
                {
                    "id": 1,
                    "name": "Survival World",
                    "version": "1.20.4",
                    "loader": "0.15.7",
                    "created_at": "2025-04-17",
                    "player_count": 6,
                    "max_players": 10,
                    "status": "online"
                },
                {
                    "id": 2,
                    "name": "Modded SMP",
                    "version": "1.19.2",
                    "loader": "0.14.11",
                    "created_at": "2025-04-01"
                },
            ]

        )


    else:
        return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/create_server", methods=["GET", "POST"])
def create_server():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        # Get form data with validation
        try:
            server_name = request.form.get('server_name', '').strip()
            if not server_name:
                flash('Server name is required', 'error')
                return redirect(url_for('dashboard.create_server'))

            # Validate and get other parameters
            mc_version = request.form.get('mc_version', '')
            loader_version = request.form.get('loader_version', '')
            installer_version = request.form.get('installer_version', '')
            motd = request.form.get('motd', 'A Minecraft Server')
            gamemode = request.form.get('gamemode', 'survival')
            difficulty = request.form.get('difficulty', 'normal')
            max_players = request.form.get('max_players', '20')
            spawn_protection = request.form.get('spawn_protection', '16')
            whitelist = request.form.get('white_list', 'false')
            pvp = request.form.get('pvp', 'off')
            server_port = request.form.get('server_port', '25565')
            online_mode = request.form.get('online_mode', 'on')

            server_env = server_eco + f"/server_eco/{server_name}"

            print("Starting to create a server...")

            # Create the server and handle errors
            success = create_server_real(server_name, mc_version, loader_version, installer_version)

            if not success:
                flash('Server creation failed', 'error')
                return redirect(url_for('dashboard.create_server'))

            print("Server Created Successfully")

            # Update server configuration
            try:
                file_manipulator(f"{server_env}/server.properties", "motd", motd)
                file_manipulator(f"{server_env}/server.properties", "gamemode", gamemode)
                file_manipulator(f"{server_env}/server.properties", "difficulty", difficulty)
                file_manipulator(f"{server_env}/server.properties", "max-players", max_players)
                file_manipulator(f"{server_env}/server.properties", "spawn-protection", spawn_protection)
                file_manipulator(f"{server_env}/server.properties", "whitelist", whitelist)
                file_manipulator(f"{server_env}/server.properties", "pvp", "true" if pvp == "on" else "false")
                file_manipulator(f"{server_env}/server.properties", "server-port", server_port)
                file_manipulator(f"{server_env}/server.properties", "online-mode","true" if online_mode == "on" else "false")
            except Exception as e:
                flash(f'Error configuring server: {str(e)}', 'error')
                # Continue anyway since the server is created

            # Redirect to the server that was just created
            # Assuming you have a way to get the server ID
            new_server_id = get_server_id_by_name(server_name)  # You'll need to implement this function
            return redirect(url_for('dashboard.server_management_server', server_id=new_server_id))

        except Exception as e:
            flash(f'Server creation error: {str(e)}', 'error')
            return redirect(url_for('dashboard.create_server'))
    else:
        # GET request handling
        if session.get('admin'):
            version = []
            loader = []
            installer = []

            # Fetch game versions with proper error handling
            try:
                with urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/game") as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        version = [{"version": i.get("version")} for i in data if i.get('stable')]
            except Exception:
                version = [
                    {"version": "1.16.5"},
                    {"version": "1.17.1"},
                    {"version": "1.18.2"},
                    {"version": "1.19.4"},
                    {"version": "1.20.1"}
                ]

            # Fetch loader versions
            try:
                with urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/loader") as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        loader = [{"loader": {"version": i.get("version")}} for i in data if i.get('stable')]
            except Exception:
                loader = [{"loader": {"version": "0.16.13"}}]

            # Fetch installer versions
            try:
                with urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/installer") as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        installer = [{"version": i.get("version")} for i in data if i.get('stable')]
            except Exception:
                installer = [{"version": "1.0.0"}]

            return render_template(
                'admin/create_server.html',
                server_properties=[
                    {'key': 'online-mode', 'name': 'Online Mode',
                     'description': 'Determines if players must authenticate with Minecraft servers.'},
                    {'key': 'spawn-protection', 'name': 'Spawn Protection',
                     'description': 'Radius of spawn protection (default 16).'},
                    {'key': 'pvp', 'name': 'PVP',
                     'description': 'Whether players can engage in player versus player combat (default true).'},
                    # Add more server properties as needed
                ],
                game_versions=version,
                loader_versions=loader,
                installer_versions=installer
            )
        else:
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/server_management/<int:server_id>", methods=["GET"])
def server_management_server(server_id):
    if 'user' not in session:
        return redirect(url_for('main.login'))

    # Dummy server data
    server = {
        'id': server_id,
        'name': 'Survival World',
        'status': 'online',  # options: 'online', 'offline', 'starting', 'stopping'
        'version': '1.19.2',
        'loader': 'Paper',
        'created_at': '2023-04-15',
        'player_count': 3,
        'max_players': 20
    }

    # Dummy templates for server creation
    templates = [
        {'id': 1, 'name': 'Vanilla 1.19.2'},
        {'id': 2, 'name': 'SkyBlock 1.18.2'},
        {'id': 3, 'name': 'PvP Factions 1.19.2'},
        {'id': 4, 'name': 'Creative 1.19.1'}
    ]

    # Dummy config files
    config_files = [
        'server.properties',
        'spigot.yml',
        'bukkit.yml',
        'paper.yml',
        'permissions.yml',
        'ops.json'
    ]

    # Dummy online players
    online_players = [
        {'name': 'Steve123', 'uuid': 'abc-123-def-456'},
        {'name': 'AlexMiner', 'uuid': 'ghi-789-jkl-012'},
        {'name': 'EnderDragon99', 'uuid': 'mno-345-pqr-678'}
    ]

    # Dummy mods/plugins
    mods = [
        {'name': 'EssentialsX', 'url': 'https://www.spigotmc.org/resources/essentialsx.9089/'},
        {'name': 'WorldEdit', 'url': 'https://dev.bukkit.org/projects/worldedit'},
        {'name': 'Vault', 'url': 'https://www.spigotmc.org/resources/vault.34315/'},
        {'name': 'LuckPerms', 'url': 'https://www.spigotmc.org/resources/luckperms.28140/'},
        {'name': 'CoreProtect', 'url': 'https://www.spigotmc.org/resources/coreprotect.8631/'}
    ]

    # Dummy performance stats
    stats = {
        'cpu': 35,
        'ram': 42,
        'disk_io': 3.8
    }

    # Dummy backups
    backups = [
        {'id': 1, 'timestamp': '2023-04-18 08:30 AM', 'size': '1.2 GB'},
        {'id': 2, 'timestamp': '2023-04-15 09:45 PM', 'size': '1.1 GB'},
        {'id': 3, 'timestamp': '2023-04-12 11:15 AM', 'size': '1.0 GB'}
    ]

    if session.get('admin'):
        return render_template(
            'admin/server_management.html',
            server=server,
            templates=templates,
            config_files=config_files,
            online_players=online_players,
            mods=mods,
            stats=stats,
            backups=backups
        )
    else:
        # Non-admin users don't have access
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('dashboard.dashboard'))
