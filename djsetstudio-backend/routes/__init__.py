from flask import Flask

from .auth import auth_bp
from .sets import sets_bp
from .tracks import tracks_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tracks_bp, url_prefix="/api/tracks")
    app.register_blueprint(sets_bp, url_prefix="/api/sets")
