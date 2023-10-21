from datetime import datetime

from flask_admin.contrib.sqla import ModelView
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
class ActivityTypeView(ModelView):
    can_delete = False
    form_columns = ["activity_type"]
    column_list = ["activity_type"]

class ActivitiesView(ModelView):
    can_delete = False
    form_columns = ["my_activity", "date", "value"]
    column_list = ["my_activity", "date", "value"]

class ActivityType(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "activity_type"
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(64), unique=True)
    activities = db.relationship("Activities", back_populates="my_activity")
    # users = db.relationship("User", back_populates="activity")

    def __init__(self, activity_type):
        self.activity_type = activity_type

    def __repr__(self):
        return self.activity_type


class Activities(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    my_activity_id = db.Column(db.ForeignKey("activity_type.id"), nullable=False)
    my_activity = db.relationship("ActivityType", back_populates="activities")
    # my_activity = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, my_activity, value):
        self.value = value
        self.my_activity = my_activity

    def __repr__(self):
        return self.my_activity

def init_activities():
    jogging_type = ActivityType("Jogging")
    pushup_type = ActivityType("Pushup")

    db.session.add(jogging_type)
    db.session.add(pushup_type)

    db.session.commit()

    first_run = Activities(jogging_type, value=10)
    second_run = Activities(jogging_type, value=15)
    first_pushup = Activities(pushup_type, value=30)
    second_pushup = Activities(pushup_type, value=34)

    db.session.add(first_run)
    db.session.add(second_run)
    db.session.add(first_pushup)
    db.session.add(second_pushup)

    db.session.commit()
