from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.plaid_client import init_plaid_client


def create_app():
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for specific resources
    CORS(app, resources={r"/plaid/*": {"origins": "http://localhost:3000"}})

    # Initialize Plaid client
    app.plaid_client = init_plaid_client(app.config)

    # Register blueprints
    from .views.plaid_views import plaid_bp
    app.register_blueprint(plaid_bp, url_prefix='/plaid')

    return app
