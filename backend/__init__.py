from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .controllers.url_controller import url_bp
    app.register_blueprint(url_bp)

    return app
