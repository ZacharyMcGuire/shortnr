from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, InputRequired, URL


class ShortUrlForm(FlaskForm):
    slug = StringField('Slug', [Length(max=7)])
    url = StringField('URL', [URL(require_tld=True, message='Please enter a valid URL'), InputRequired()])
