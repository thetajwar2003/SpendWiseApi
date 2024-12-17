from app import create_app
import os

# Load the environment configuration
ENV = os.getenv("FLASK_ENV", "development")  # Default to "development"

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Get PORT dynamically from environment or fallback to 5000
    port = int(os.environ.get("PORT", 5000))

    # Set the host to "0.0.0.0" for Heroku compatibility
    if ENV == "development":
        # Run the app in development mode with debugging enabled
        app.run(host="127.0.0.1", port=port, debug=True)
    elif ENV == "production":
        # Run the app in production mode
        app.run(host="0.0.0.0", port=port)
    else:
        raise ValueError(
            "Invalid FLASK_ENV value. Must be 'development' or 'production'.")
