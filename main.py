import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

from functions.initial.initial_script import initial_script

from functions.database.database_alc import User, session as db_session


app = Flask(__name__)
app.secret_key = os.urandom(24)


# Dummy credentials
USERNAME = 'isma'
PASSWORD = '1234'


initial_script()


@app.route("/")
def home():

    # Dummy mods list
    mods = [
        {"name": "Baubles",        "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty",   "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        # … potentially hundreds more …
    ]

    return render_template(
        "index.html",
        user_name="Isma",
        server_ip="play.example.com",
        server_port=25565,
        active_players=12,
        mc_version="1.20.4",
        total_mods=32,
        uptime="4 days, 3 hours",
        mods=mods
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']

        # Query the database to find the user by email
        user = db_session.query(User).filter_by(name=user_name).first()

        if user and user.password == password:  # Check if user exists and password matches
            session['user'] = user_name  # Store user email or ID in session
            session['admin'] = True if user.is_admin else False

            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

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


@app.route('/dashboard/server_management')
def server_management():
    if 'user' not in session:
        return redirect(url_for('login'))

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
                    "created_at": "2025-04-17"
                },
                {
                    "id": 2,
                    "name": "Modded SMP",
                    "version": "1.19.2",
                    "loader": "0.14.11",
                    "created_at": "2025-04-01"
                },
                {
                    "id": 3,
                    "name": "Creative Server",
                    "version": "1.18.2",
                    "loader": "0.14.8",
                    "created_at": "2025-03-12"
                }
            ]

        )
        # return render_template(
        #     "admin/server_management.html",
        #         user_name="Isma",
        #         templates=[
        #             {"id": "vanilla-1.20.1", "name": "Vanilla 1.20.1"},
        #             {"id": "paper", "name": "PaperMC"}
        #         ],
        #         config_files=["server.properties", "bukkit.yml", "whitelist.json"],
        #         online_players=[
        #             {"name": "Steve"},
        #             {"name": "Alex"}
        #         ],
        #         mods=[
        #             {"name": "JourneyMap", "url": "https://www.curseforge.com/journeymap"},
        #             {"name": "WorldEdit", "url": "https://enginehub.org/worldedit"}
        #         ],
        #         stats={
        #             "cpu": 23,
        #             "ram": 62,
        #             "disk_io": 1.2
        #         },
        #         backups=[
        #             {"id": "b1", "timestamp": "2025-04-17 22:45"},
        #             {"id": "b2", "timestamp": "2025-04-16 18:20"}
        #         ],
        #         server={
        #             "id": "main-survival"}
        #         )

    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard/create_server')
def create_server():
    return render_template(
        'admin/create_server.html',
        server_properties=[
            {'key': 'online-mode', 'name': 'Online Mode', 'description': 'Determines if players must authenticate with Minecraft servers.'},
            {'key': 'spawn-protection', 'name': 'Spawn Protection',
             'description': 'Radius of spawn protection (default 16).'},
            {'key': 'pvp', 'name': 'PVP',
             'description': 'Whether players can engage in player versus player combat (default true).'},
            # Add more server properties as needed
        ],
        # Dummy data for rendering
        game_versions=[
            {"version": "1.16.5"},
            {"version": "1.17.1"},
            {"version": "1.18.2"},
            {"version": "1.19.4"},
            {"version": "1.20.1"},
        ],
        loader_versions = [
            {"loader": {"version": "0.11.3"}},
            {"loader": {"version": "0.11.4"}},
            {"loader": {"version": "0.11.5"}},
        ],
        installer_versions = [
            {"version": "1.0.0"},
            {"version": "1.1.0"},
            {"version": "1.2.0"},
            {"version": "2.0.0"},
        ]
    )

@app.route('/edit_file', methods=['POST'])
def edit_file():
    return render_template(
        '404.html'
    )

@app.route('/server_action', methods=['POST'])
def server_action():
    return render_template(
        '404.html'
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Custom error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
