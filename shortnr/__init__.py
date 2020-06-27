import os
from nanoid import generate
from flask import Flask, request
from flask_mongoengine import MongoEngine


def create_app(test_config=None):
    db = MongoEngine()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        MONGODB_DB=os.environ.get('MONGODB_DB'),
        MONGODB_USERNAME=os.environ.get('MONGODB_USERNAME'),
        MONGODB_PASSWORD=os.environ.get('MONGODB_PASSWORD'),
    )
    db.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello, World!!"

    @app.route('/create', methods=["POST"])
    def create_short_url():
        """Create a new shortened URL and return it."""
        req_data = request.get_json()
        url = req_data['url']
        if 'slug' in req_data:
            slug = req_data['slug']
        else:
            slug = generate(size=7)

        return slug

    return app
