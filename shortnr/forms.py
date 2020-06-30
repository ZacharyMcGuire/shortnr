from flask_wtf import FlaskForm
from wtforms.validators import data_required, url, length
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField


class ShortUrlForm(FlaskForm):
    url = URLField(u'Enter a URL', validators=[
        data_required(),
        url()
    ])
