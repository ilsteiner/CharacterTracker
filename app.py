#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
from flask_wtf import CsrfProtect
from sqlalchemy import exc

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
csrf = CsrfProtect(app)
app.config.from_object('config')
db = SQLAlchemy(app)

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
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    session = db_session()
    characters = session.query(Character).all()
    return render_template('pages/home.html', characters=characters)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/new-character', methods=['GET', 'POST'])
def new_character():
    form = NewCharacterForm(request.form)

    for relationship in form.relationships:
        relationship.related_to.query = Character.query

    if form.validate_on_submit():
        session = db_session()

        character = Character(form.name.data, form.short_description.data, form.description.data)

        try:
            session.add(character)
            session.flush()
            session.refresh(character)

            # If there are characters to be related to and thus the relationship form was displayed
            if character_count() > 1:
                for relationship in form.relationships:
                    # If the related to dropdown is not blank
                    if relationship.related_to.data:
                        new_relationship = Relationship(character.id, relationship.related_to.data.id,
                                                        relationship.relationship_type.data,
                                                        relationship.relationship_description.data)
                        session.add(new_relationship)
                        session.flush()
        except (exc.IntegrityError, exc.InvalidRequestError) as e:
            session.rollback()
            flash(e.message)

    else:
        for fieldName, errorMessages in form.errors.iteritems():
            for err in errorMessages:
                flash(err)

    return render_template('forms/new-character.html', form=form, character_count=character_count())


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
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
