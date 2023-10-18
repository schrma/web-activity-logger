import os

import activity_logger.users.views
import sqlalchemy as sa
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from activity_logger.models import User, BlogPost, db

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
login_manager = LoginManager()
login_manager.login_view = "users.login"
admin = Admin()

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    initialize_admin(app)
    return app

def register_blueprints(app):
    ###########################
    #### BLUEPRINT CONFIGS #######
    #########################

    # Import these at the top if you want
    # We've imported them here for easy reference
    from activity_logger.blog_posts.views import blog_posts
    from activity_logger.core.views import core
    from activity_logger.error_pages.handlers import error_pages
    from activity_logger.users.views import users_blueprint

    # Register the apps
    app.register_blueprint(users_blueprint)
    app.register_blueprint(blog_posts)
    app.register_blueprint(core)
    app.register_blueprint(error_pages)

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    Migrate(app,db)
    login_manager.init_app(app)

def initialize_admin(app):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(BlogPost, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
