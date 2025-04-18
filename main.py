import os
from dotenv import load_dotenv

from flask import Flask, render_template

from functions.initial.initial_script import initial_script


from routes.api_server import api_server_bp
from routes.dashboard import dashboard_bp
from routes.main import main_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)



initial_script()

# Register all blueprints
app.register_blueprint(main_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_server_bp)

# Custom error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
