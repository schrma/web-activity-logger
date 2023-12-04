from datetime import datetime

from flask_login import UserMixin

from activity_logger.models import BaseUserModelView
from activity_logger.models.org import User, db

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


class UnitTypeView(BaseUserModelView):
    can_delete = True
    form_columns = ["unit_type"]
    column_list = ["unit_type"]


class UnitType(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "unit_type"
    id = db.Column(db.Integer, primary_key=True)
    unit_type = db.Column(db.String(64), unique=True)
    units = db.relationship("Activities", back_populates="my_unit")

    def __init__(self, unit_type):
        self.unit_type = unit_type

    def __repr__(self):
        return self.unit_type


class ActivityTypeView(BaseUserModelView):
    can_delete = True
    form_columns = ["activity_type"]
    column_list = ["activity_type"]


class ActivitiesView(BaseUserModelView):
    can_delete = True
    form_columns = ["my_user", "my_activity", "value", "my_unit", "date"]
    column_list = ["my_user", "my_activity", "value", "my_unit", "date"]


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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    my_unit_id = db.Column(db.ForeignKey("unit_type.id"), nullable=False)
    my_unit = db.relationship("UnitType", back_populates="units")

    my_user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    my_user = db.relationship("User", back_populates="user_activities")

    def __init__(self, my_activity, value, my_unit, my_user):
        self.value = value
        self.my_activity = my_activity
        self.my_unit = my_unit
        self.my_user = my_user

    def __repr__(self):
        return self.my_activity


def init_activities():
    jogging_type = ActivityType("Jogging")
    pushup_type = ActivityType("Pushup")
    km_type = UnitType("km")
    times_type = UnitType("X")

    db.session.add(jogging_type)
    db.session.add(pushup_type)
    db.session.add(km_type)
    db.session.add(times_type)

    db.session.commit()

    user_one = User.query.filter_by(username="one").first()
    user_two = User.query.filter_by(username="two").first()

    first_run = Activities(
        my_activity=jogging_type, value=11.11, my_unit=km_type, my_user=user_one
    )
    second_run = Activities(
        my_activity=jogging_type, value=12.22, my_unit=km_type, my_user=user_one
    )
    first_pushup = Activities(
        my_activity=pushup_type, value=13.33, my_unit=times_type, my_user=user_two
    )
    second_pushup = Activities(
        my_activity=pushup_type, value=14.44, my_unit=times_type, my_user=user_two
    )

    db.session.add(first_run)
    db.session.add(second_run)
    db.session.add(first_pushup)
    db.session.add(second_pushup)

    db.session.commit()
