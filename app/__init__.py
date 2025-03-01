from flask import Flask

app = Flask(__name__)

from app.routes import bp as routes_bp
app.register_blueprint(routes_bp)

from app import routes
