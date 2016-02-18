import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'tB3*fHq2Xp@VZv#Hw65p2be^fZ#SGaOWYRNSCYCSu^*bkh7YqM'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True
