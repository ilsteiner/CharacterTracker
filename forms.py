from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length

# Set your classes here.


class NewCharacterForm(Form):
    name = StringField(
        'Character Name', validators=[DataRequired(), Length(min=1, max=120)]
    )

    short_description = StringField(
        'Short Description', validators=[DataRequired(), Length(min=1, max=256)]
    )

    description = TextAreaField(
        'Character Description', validators=[DataRequired(), Length(min=10, max=10000)]
    )

    related_to = QuerySelectField(get_label='name')


class NewRelationshipTypeForm(Form):
    description = StringField(
        'Relationship Type', validators=[DataRequired(), Length(min=1, max=120)]
    )
