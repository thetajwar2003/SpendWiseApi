from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.aws_dynamodb import init_dynamodb
from .utils.aws_cognito import init_cognito
from .utils.plaid_client import init_plaid_client


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize AWS services
    app.dynamodb = init_dynamodb(app.config)
    app.cognito = init_cognito(app.config)
    app.plaid_client = init_plaid_client(app.config)

    # Register blueprints
    from .views.auth_views import auth_bp
    from .views.transaction_views import transaction_bp
    from .views.budget_views import budget_bp
    from .views.subscription_views import subscription_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(budget_bp, url_prefix='/budgets')
    app.register_blueprint(subscription_bp, url_prefix='/subscriptions')

    return app
