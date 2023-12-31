import os
from datetime import timedelta

import sqlalchemy as sa
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_migrate import Migrate

from activity_logger.models.db_activites import (
    Activities,
    ActivitiesView,
    ActivityType,
    ActivityTypeView,
    UnitType,
    UnitTypeView,
)
from activity_logger.models.org import BlogPost, Role, RoleView, User, UserView, db

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
login_manager = LoginManager()
login_manager.login_view = "users.login"
admin = Admin()
# dash_app = None


def create_app():
    # global dash_app
    # Create the Flask application
    app = Flask(__name__)

    # Import Dash application
    from .dashboard import init_dashboard  # pylint: disable=import-outside-toplevel

    app = init_dashboard(app)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        app.logger.info("Use flask init-db")
        with app.app_context():
            db.create_all()
    else:
        app.logger.info("Database already contains the users table.")

    with app.app_context():
        register_blueprints(app)
    app.permanent_session_lifetime = timedelta(days=14)

    initialize_admin(app)
    return app


def register_blueprints(app):
    # Import these at the top if you want
    # We've imported them here for easy reference
    from activity_logger.blog_posts.views import (  # pylint: disable=import-outside-toplevel
        blog_posts,
    )
    from activity_logger.core.views import (  # pylint: disable=import-outside-toplevel
        core,
    )
    from activity_logger.error_pages.handlers import (  # pylint: disable=import-outside-toplevel
        error_pages,
    )
    from activity_logger.users.views import (  # pylint: disable=import-outside-toplevel
        users_blueprint,
    )

    # Register the apps
    app.register_blueprint(users_blueprint)
    app.register_blueprint(blog_posts)
    app.register_blueprint(core)
    app.register_blueprint(error_pages)


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)


def initialize_admin(app):
    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(ModelView(BlogPost, db.session))
    admin.add_view(ActivityTypeView(ActivityType, db.session))
    admin.add_view(ActivitiesView(Activities, db.session))
    admin.add_view(UnitTypeView(UnitType, db.session))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
