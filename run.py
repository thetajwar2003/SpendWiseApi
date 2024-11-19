from app import create_app
import os

# Load the environment configuration
ENV = os.getenv("FLASK_ENV", "development")  # Default to "development"

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    if ENV == "development":
        # Run the app in development mode with debugging enabled
        app.run(host="127.0.0.1", port=5000, debug=True)
    elif ENV == "production":
        # Run the app in production mode
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    else:
        raise ValueError(
            "Invalid FLASK_ENV value. Must be 'development' or 'production'.")
