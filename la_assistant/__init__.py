import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # take environment variables from .env.


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'la_assistant.sqlite')
    )

    if os.getenv('IS_DEV_MODE'):
        CORS(app, supports_credentials=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import assistant
    app.register_blueprint(assistant.bp)

    from . import user
    app.register_blueprint(user.bp)

    return app
