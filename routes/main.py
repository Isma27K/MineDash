from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from functions.database.database_alc import User, session as db_session


main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home():

    # Dummy mods list
    mods = [
        {"name": "Baubles",        "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
        {"name": "Biomes O' Plenty",   "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
        {"name": "Baubles", "url": "https://www.curseforge.com/minecraft/mc-mods/baubles"},
        {"name": "Tinkers' Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
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
