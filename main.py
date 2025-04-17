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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

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
