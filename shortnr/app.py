import datetime
import os
import click
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from nanoid import generate
from sqlalchemy import exc
from sqlalchemy_utils import URLType
from shortnr import forms

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)


class Url(db.Model):
    slug = db.Column(db.String(7), primary_key=True)
    url = db.Column(URLType)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return self.slug


@app.route('/', methods=['GET'])
def index():
    """Website root URL. Present the ShortUrlForm."""
    form = forms.ShortUrlForm()
    return render_template('index.html', form=form)


@app.route('/create', methods=["POST"])
def create_short_url():
    """Create a new shortened URL and return it."""
    req_data = request.form
    url = req_data['url']
    if 'slug' in req_data and req_data['slug'] != '':
        slug = req_data['slug']
    else:
        slug = generate(size=7)

    record = Url(slug=slug, url=url)
    db.session.add(record)
    db.session.commit()

    return f'{request.url_root}{slug}'


@app.route('/<slug>', methods=["GET"])
def redirect_from_short_url(slug):
    """Lookup the provided slug in the db and redirect to the URL, or route back to URL root."""
    try:
        record = Url.query.filter_by(slug=slug).first()
        redirect_url = record.url
        return redirect(redirect_url, 308)
    except AttributeError:
        return '404'


@app.cli.command('wait-for-db')
def wait_for_db_command():
    """Command to pause execution until database is available"""
    from sqlalchemy_utils import database_exists

    db_conn = None
    while not db_conn:
        try:
            database_exists(os.environ.get('DATABASE_URI'))
        except exc.OperationalError:
            print('Database unavailable. Trying again...')
            pass
        finally:
            print('Database available.')
            db_conn = True


@app.cli.command('init-db')
@click.option("--reinitialise", default=False, help="Set to True if you wish to reinitialise the database.",
              show_default=True, type=bool)
def init_db_command(reinitialise=False):
    """optionally drops existing database. Creates the database + tables"""
    from sqlalchemy_utils import database_exists, create_database, drop_database

    wait_for_db_command

    if database_exists(os.environ.get('DATABASE_URI')) and reinitialise:
        print('DROPPING CURRENT DATABASE')
        drop_database(os.environ.get('DATABASE_URI'))

    if not database_exists(os.environ.get('DATABASE_URI')):
        print('CREATING NEW DATABASE')
        create_database(os.environ.get('DATABASE_URI'))

    print('CREATING DATABASE SCHEMA')
    db.create_all()

    print('DATABASE INITIALISED')
