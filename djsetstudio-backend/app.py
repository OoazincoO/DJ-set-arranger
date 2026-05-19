"""DJsetStudio Backend - app entry.

This module exposes `create_app()` for WSGI servers and allows running via
`python app.py` during development.
"""

from dotenv import load_dotenv

load_dotenv()

from flask import Flask

from config import get_config
from extensions import cors, db, jwt
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # init extensions
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # register routes
    register_blueprints(app)

    # health check
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    # create tables in dev (safe for sqlite demo; for prod use migrations)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
