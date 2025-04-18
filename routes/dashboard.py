import json
import os

from flask import Blueprint, session, redirect, url_for, render_template, request, flash, jsonify
import urllib.request

from starlette.responses import JSONResponse
from werkzeug.utils import secure_filename

from functions.database.database_alc import User, Servers, db_session, Mods

from functions.database.db_related import get_server_id_by_name
from functions.minecraft_management.management import create_server_real
from utils.file import file_manipulator
from utils.system_util import cpu_percent, used_ram_percent, avg_io_mb

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
        server_list = []
        server = db_session.query(Servers).all()

        for s in server:
            server_list.append({
                'id': s.id,
                'name': s.name,
                'version': s.mc_version,
                'loader': s.loader_version,
                'created_at': s.created_at,
                'player_count': 1,
                'max_players': s.max_players,
                'status': "online" if s.status else "offline",
            })

        return render_template(
            'admin/server_list.html',
            # Example data to simulate server list
            servers=server_list
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

            server = db_session.query(Servers).filter(Servers.name == server_name).first()
            if server is not None:
                flash('Server name already exists', 'error')
                return redirect(url_for('dashboard.create_server'))

            print("Starting to create a server...")

            # Create the server and handle errors
            success = create_server_real(server_name, mc_version, loader_version, installer_version)

            # try to save to database
            user = db_session.query(User).filter_by(name=session['user']).first()
            new_db = Servers(
                name=server_name, mc_version=mc_version, loader_version=loader_version,
                installer_version=installer_version, motd=motd, gamemode=gamemode, difficulty=difficulty,
                max_players=int(max_players), port=int(server_port), created_by=user.id
            )

            db_session.add(new_db)
            db_session.commit()

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

    server = db_session.query(Servers).filter(Servers.id == server_id).first()
    server_mods = db_session.query(Mods).filter(Mods.server_belongs == server_id).all()

    server = {
        'id': server_id,
        'name': server.name,
        'status': 'online' if server.status else 'offline',  # options: 'online', 'offline', 'starting', 'stopping'
        'version': server.mc_version,
        'loader': server.loader_version,
        'created_at': server.created_at,
        'player_count': 3,
        'max_players': server.max_players
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

    mods = []

    for mod in server_mods:
        mods.append({'name': mod.name, 'url': mod.url, 'id': mod.id, "server_id": mod.server_belongs})

    # Dummy performance stats
    stats = {
        'cpu': cpu_percent,
        'ram': used_ram_percent,
        'disk_io': avg_io_mb
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


@dashboard_bp.route("/mods/<int:server_id>", methods=["GET"])
def upload_mods_page(server_id):

    if 'user' not in session:
        return redirect(url_for('main.login'))

    server_data = db_session.query(Servers).filter(Servers.id == server_id).first()

    server = {
        "id": server_id,
        "name": server_data.name,
        "version": server_data.mc_version,
        "loader": server_data.loader_version,
        "status": "online" if server_data.status else "offline",
        "created_at": server_data.created_at,
        "player_count": 3,
        "max_players": server_data.max_players,
    }

    return render_template(
        'add_mods.html',
        server=server,
    )


@dashboard_bp.route("/server_management/<int:server_id>/add_mods", methods=["POST"])
def upload_mods(server_id):
    ALLOWED_EXTENSIONS = {'jar'}

    # Get server info once
    server = db_session.query(Servers).filter(Servers.id == server_id).first()
    if server is None:
        flash('Server not found', 'error')
        return redirect(url_for('dashboard.dashboard'))

    # Define upload path using server name
    # Assuming server_eco is defined elsewhere - if not, define it appropriately
    UPLOAD_FOLDER = os.path.join(server_eco, "server_eco", server.name, "mods")

    # Create function to check file extensions
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Ensure the folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Get current user
    user = db_session.query(User).filter_by(name=session.get('user')).first()
    if not user:
        flash('User not authenticated', 'error')
        return redirect(url_for('auth.login'))

    uploaded_files = request.files.getlist('mod_files')
    mod_names = request.form.getlist('mod_names[]')
    mod_versions = request.form.getlist('mod_versions[]')
    mod_links = request.form.getlist('mod_links[]')
    mod_descriptions = request.form.getlist('mod_descriptions[]')

    if not uploaded_files or uploaded_files[0].filename == '':
        flash('No mod files uploaded', 'error')
        return redirect(url_for('dashboard.upload_mods_page', server_id=server_id))

    successful_uploads = 0

    for idx, file in enumerate(uploaded_files):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            # Use safer list access with default values
            mod_name = mod_names[idx] if idx < len(mod_names) else filename
            mod_version = mod_versions[idx] if idx < len(mod_versions) else ""
            mod_link = mod_links[idx] if idx < len(mod_links) else ""
            mod_description = mod_descriptions[idx] if idx < len(mod_descriptions) else ""

            # Create and save mod to database
            try:
                new_mod = Mods(
                    name=filename,  # Fixed from mod_info.name
                    url=mod_link,  # Fixed from mods_info.link
                    server_belongs=server.id,
                    add_by=user.id,
                    version=mod_version,
                    description=mod_description
                )
                db_session.add(new_mod)
                db_session.commit()
                successful_uploads += 1
            except Exception as e:
                db_session.rollback()
                flash(f'Error saving mod to database: {str(e)}', 'error')
                # Continue to next file instead of stopping completely
                continue
        else:
            flash(f'Invalid file type for {file.filename if file.filename else "unnamed file"}', 'error')

    if successful_uploads > 0:
        flash(f'Successfully uploaded {successful_uploads} mod(s)', 'success')

    return redirect(url_for('dashboard.server_management_server', server_id=server_id))