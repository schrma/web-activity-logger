from datetime import datetime

from flask_login import UserMixin

from activity_logger.models.org import db

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.


class ActivityType(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "activity_type"
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(64), unique=True)
    # users = db.relationship("User", back_populates="activity")

    def __init__(self, activity):
        self.activity = activity

    def __repr__(self):
        return self.activity


class Activities(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    my_activity = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, my_activity, value):
        self.my_activity = my_activity
        self.value = value

    def __repr__(self):
        return self.my_activity


def init_activity_type():
    jogging_type = ActivityType("Jogging")
    pushup_type = ActivityType("Pushup")

    db.session.add(jogging_type)
    db.session.add(pushup_type)

    db.session.commit()


def init_activities():
    init_activity_type()

    first_run = Activities(my_activity="Jogging", value=10)
    second_run = Activities(my_activity="Jogging", value=15)
    first_pushup = Activities(my_activity="Pushup", value=30)
    second_pushup = Activities(my_activity="Pushup", value=34)

    db.session.add(first_run)
    db.session.add(second_run)
    db.session.add(first_pushup)
    db.session.add(second_pushup)

    db.session.commit()
