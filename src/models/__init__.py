from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance to be used across the application
db = SQLAlchemy()

# Do not import models here to avoid circular imports
# Import models directly from their respective files in other modules
