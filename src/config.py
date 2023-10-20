import os

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
FOLDER_DB = "folder_db"


def create_folder_for_database_if_not_exists():
    folder_to_create = os.path.join(BASEDIR, FOLDER_DB)
    if not os.path.exists(folder_to_create):
        os.makedirs(folder_to_create)


create_folder_for_database_if_not_exists()


class Config:  # pylint: disable=too-few-public-methods
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    # Since SQLAlchemy 1.4.x has removed support for the 'postgres://' URI scheme,
    # update the URI to the postgres database to use the supported 'postgresql://' scheme
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace(
            "postgres://", "postgresql://", 1
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, FOLDER_DB, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    FLASK_ENV = "production"


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    DEBUG = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI", default=f"sqlite:///{os.path.join(BASEDIR, FOLDER_DB, 'test.db')}"
    )
