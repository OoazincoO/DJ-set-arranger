from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Extension instances (initialized in app factory)
db = SQLAlchemy()
jwt = JWTManager()

# CORS origins can be configured via app.config['CORS_ORIGINS']
cors = CORS()
