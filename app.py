# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, jsonify, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from forms import *
from models import *
from flask_wtf import CsrfProtect
from sqlalchemy import exc, or_
import os
from random import sample, randint
from urllib import quote_plus, unquote_plus

# from graph import make_graph

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
csrf = CsrfProtect(app)
app.config.from_object('config')
db = SQLAlchemy(app)

current_directory = os.path.dirname(__file__)

app.secret_key = 'tB3*fHq2Xp@VZv#Hw65p2be^fZ#SGaOWYRNSCYCSu^*bkh7YqM'

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def home():
    session = db_session()
    characters = session.query(Character).all()
    form = SearchCharacterForm(request.form)
    return render_template('pages/home.html', characters=characters, form=form)


@app.route('/graph-query.json', methods=['GET'])
def graph_query():
    names = request.args.get('name')
    if names is None:
        names = []
    graph = make_graph(names)
    return jsonify(results=graph)


@app.route('/populate-data', methods=['POST'])
def populate_data():
    populate_sample_data()
    return redirect('/', code=302)


@csrf.exempt
@app.route('/search-characters', methods=['POST'])
def search_characters():
    session = db_session()

    data = request.get_json()

    name = data.get("name")

    description_snippet = data.get("description_snippet")

    results = session.query(Character).filter(Character.name.contains(name),
                                              or_(
                                                      Character.short_description.contains(description_snippet),
                                                      Character.description.contains(description_snippet)
                                              )).all()

    characters = []

    session.close()

    for character in results:
        characters.append(
                {'id': character.id, 'name': character.name, 'short_description': character.short_description})

    return jsonify(characters=characters)


@app.route('/characters/<character_id>', methods=['GET', 'POST'])
def view_character_id(character_id):
    session = db_session()
    character = session.query(Character).get(int(character_id))
    form = CharacterForm(request.form)
    form.character = character
    form.name.data = character.name
    form.short_description.data = character.short_description
    form.description.data = character.description

    relationships = session.query(Relationship).filter(Relationship.primary == character.id).all()

    reverse_relationships = session.query(Relationship).filter(Relationship.related_to == character_id).all()

    for relationship in relationships:
        reverse_relationship_type = ''
        reverse_relationship_description = ''

        for reverse_relationship in reverse_relationships:
            if reverse_relationship.primary == relationship.related_to:
                reverse_relationship_type = reverse_relationship.relationship_type
                reverse_relationship_description = reverse_relationship.relationship_description

        if reverse_relationship_type != '':
            form.relationships.append_entry({'related_to': relationship.related_to,
                                             'relationship_type': relationship.relationship_type,
                                             'relationship_description': relationship.relationship_description,
                                             'bidirectional': True,
                                             'other_relationship_type': reverse_relationship_type,
                                             'other_relationship_description': reverse_relationship_description
                                             })
        else:
            form.relationships.append_entry({'related_to': relationship.related_to,
                                             'relationship_type': relationship.relationship_type,
                                             'relationship_description': relationship.relationship_description})

    for relationship in form.relationships:
        relationship.related_to.query = Character.query

    session.close()
    return render_template('forms/character.html', form=form, character_count=character_count())


@app.route('/new-character', methods=['GET', 'POST'])
def new_character():
    form = CharacterForm(request.form)

    for relationship in form.relationships:
        relationship.related_to.query = Character.query

    if form.validate_on_submit():
        session = db_session()

        character = Character(form.name.data, form.short_description.data, form.description.data)

        try:
            session.add(character)
            session.commit()
            flash(character.name + ' created')

            # If there are characters to be related to and thus the relationship form was displayed
            if character_count() > 1:
                new_relationships = 0
                for relationship in form.relationships:
                    # If the related to dropdown is not blank
                    if relationship.related_to.data:
                        new_relationship = Relationship(character.id, relationship.related_to.data.id,
                                                        relationship.relationship_type.data,
                                                        relationship.relationship_description.data)
                        session.add(new_relationship)
                        session.commit()
                        new_relationships += 1

                if new_relationships == 1:
                    flash('Created ' + str(new_relationships) + ' new character relationship')
                elif new_relationships > 0:
                    flash('Created ' + str(new_relationships) + ' new character relationships')

            session.close()
        except (exc.IntegrityError, exc.InvalidRequestError) as e:
            session.rollback()
            flash(e.message)

    else:
        for fieldName, errorMessages in form.errors.iteritems():
            for err in errorMessages:
                flash(err)

    return render_template('forms/character.html', form=form, character_count=character_count())


# @app.route('/new-relationship-type', methods=['GET', 'POST'])
# def new_relationship_type():
#     form = NewRelationshipTypeForm(request.form)
#
#     session = db_session()
#
#     try:
#         if form.validate_on_submit():
#             new_type = RelationshipType(form.description.data)
#             session.add(new_type)
#             session.commit()
#
#         else:
#             for fieldName, errorMessages in form.errors.iteritems():
#                 for err in errorMessages:
#                     flash(err)
#     except exc.IntegrityError:
#             session.rollback()
#             flash('Must be unique.')
#
#     return render_template('forms/new-relationship-type.html', form=form)
# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)
#
#
# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)
#
#
# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    error_log = os.path.join(current_directory, 'error.log')

    file_handler = RotatingFileHandler(error_log, maxBytes=10000, backupCount=1)

    file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


def populate_sample_data():
    sample_names_file = os.path.join(current_directory, 'sample_names.txt')

    session = db_session()

    try:
        with open(sample_names_file) as sample_names:
            just_names = (line.rstrip('\n') for line in sample_names)
            for name in just_names:
                character = Character(name, "This a short description of " + name,
                                      "This is a long description of " + name)

                session.add(character)
                session.commit()

        characters = session.query(Character).all()

        for character in characters:
            related_characters = sample(characters, randint(0, 5))

            for related_character in related_characters:
                relationship = Relationship(character.id, related_character.id, 'Friend', 'They are just friends')
                if related_character.id != character.id:
                    session.add(relationship)
                session.commit()

        session.close()

    except exc.IntegrityError as e:
        session.rollback()
        app.logger.info('Could not insert ' + name + ': ' + e.message)


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.run()
    else:
        app.run(host='0.0.0.0', port=port)
