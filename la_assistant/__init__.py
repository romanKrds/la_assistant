import os
from flask import Flask

from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv('.env.mysql.env')  # take environment variables from .env.

host = os.getenv("MYSQL_HOST")
username = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database_name = os.getenv("MYSQL_DATABASE")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{username}:{password}@{host}/{database_name}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if os.getenv('FLASK_ENV') == 'development':
        CORS(app, supports_credentials=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    from .blueprints import auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints import user_bp
    app.register_blueprint(user_bp)

    from .blueprints import vocabulary_bp
    app.register_blueprint(vocabulary_bp)

    return app
