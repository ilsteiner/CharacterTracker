from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class NewCharacterForm(Form):
    name = TextField(
        'Character Name', validators=[DataRequired(), Length(min=1, max=120)]
    )

    short_description = TextField(
        'Short Description', validators=[DataRequired(), Length(min=10, max=256)]
    )

    description = TextAreaField(
        'Character Description', validators=[DataRequired(), Length(min=10, max=10000)]
    )
