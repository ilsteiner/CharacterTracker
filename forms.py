from flask_wtf import Form
from wtforms import StringField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Required, Optional
from models import Character

# Set your classes here.


class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class RelationshipForm(Form):
    related_to = QuerySelectField(get_label='name', validators=[Optional()])

    related_to.query = Character.query

    relationship_type = StringField(
        'Relationship Type', validators=[RequiredIf('related_to')]
    )

    relationship_description = TextAreaField(
        'Relationship Description', validators=[RequiredIf('related_to')]
    )

    bidirectional = BooleanField(
        'Bidirectional?'
    )

    other_relationship_type = StringField(
        'Relationship Type', validators=[RequiredIf('related_to')]
    )

    other_relationship_description = StringField(
        'Relationship Description', validators=[RequiredIf('related_to')]
    )


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

    relationships = FieldList(FormField(RelationshipForm), validators=[Optional()], min_entries=1)

# class NewRelationshipTypeForm(Form):
#     description = StringField(
#         'Relationship Type', validators=[DataRequired(), Length(min=1, max=120)]
#     )
