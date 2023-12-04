from flask.cli import with_appcontext

from activity_logger import create_app
from activity_logger.models.build import build_default_database
from activity_logger.models.org import db

app = create_app()

if __name__ == "__main__":
    # app = create_app()
    app.run(debug=True)


@app.cli.command("init-db")
@with_appcontext
def init_db_command():
    with app.app_context():
        db.drop_all()
        db.create_all()
        build_default_database()

    print("Default data has been written to the database.")
