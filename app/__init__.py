from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.plaid_client import init_plaid_client
from .utils.aws_cognito import init_cognito
from .utils.aws_dynamodb import init_dynamodb


def create_app():
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for specific resources
    # CORS(app, resources={r"/plaid/*": {"origins": "http://localhost:3000"},
    #      r"/auth/*": {"origins": "http://localhost:3000"}})
    CORS(app)

    # Initialize AWS services
    app.plaid_client = init_plaid_client(app.config)  # Initialize Plaid client
    app.cognito = init_cognito(app.config)  # Initialize Cognito client
    app.dynamodb = init_dynamodb(app.config)  # Initialize DynamoDB client

    # Register blueprints
    from .views.plaid_views import plaid_bp
    from .views.auth_views import auth_bp

    app.register_blueprint(plaid_bp, url_prefix='/plaid')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
