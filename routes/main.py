from urllib.parse import urlparse

from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from functions.database.database_alc import User, db_session as db_session, Servers, Mods
from functions.state import global_holder

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    # Default values when no server is online
    server_ip = "No server online"
    server_port = None
    active_players = 0
    mc_version = "N/A"
    total_mods = 0
    mods = []

    # Try to get an active server
    server = db_session.query(Servers).filter(Servers.status == True).first()

    if server:
        # If a server exists, get its mods
        server_mods = db_session.query(Mods).filter(Mods.server_belongs == server.id).all()

        # Process mods if there are any
        if server_mods:
            mods = [{"name": mod.name, "url": mod.url} for mod in server_mods]
            total_mods = len(mods)

        # Set Minecraft version
        mc_version = server.mc_version

        # Try to get the ngrok URL if active
        try:
            if hasattr(global_holder, 'active_listener') and global_holder.active_listener:
                server_ip = global_holder.active_listener.url()
            else:
                server_ip = "Tunnel not established"
        except Exception as e:
            server_ip = "Tunnel error"
            print(f"Error getting tunnel URL: {str(e)}")

        # Extract the port from the server_ip
        try:
            parsed = urlparse(server_ip)
            server_port = parsed.port
        except Exception as e:
            print(f"Error parsing server IP: {str(e)}")
            server_port = None

    return render_template(
        "index.html",
        user_name="Isma",
        server_ip=server_ip,
        server_port=server_port,
        active_players=active_players,
        mc_version=mc_version,
        total_mods=total_mods,
        uptime="Feature coming soon",
        mods=mods
    )

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']

        # Query the database to find the user by email
        user = db_session.query(User).filter_by(name=user_name).first()

        if user and user.password == password:  # Check if user exists and password matches
            session['user'] = user_name  # Store user email or ID in session
            session['admin'] = True if user.is_admin else False

            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

@main_bp.route("/logout", methods=["GET"])
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))
