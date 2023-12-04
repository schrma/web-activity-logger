from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from activity_logger.models import BaseAdminModelView

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

db = SQLAlchemy()


class RoleView(BaseAdminModelView):
    can_delete = False
    form_columns = ["role"]
    column_list = ["role"]


class Role(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), unique=True)
    users = db.relationship("User", back_populates="role")

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return self.role


class UserView(BaseAdminModelView):
    can_delete = True
    form_columns = ["username", "email", "role"]
    column_list = ["username", "email", "role"]


class User(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default="default_profile.png")
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")
    user_activities = db.relationship("Activities", back_populates="my_user")
    # This connects BlogPosts to a User Author.
    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


class BlogPost(db.Model):  # pylint: disable=too-few-public-methods
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"


def init_user():
    admin_role = Role("Admin")
    user_role = Role("User")

    db.session.add(admin_role)
    db.session.add(user_role)

    db.session.commit()
    # Insert user data
    default_user = User(username="one", email="one@one.com", password="my_secret")
    second_user = User(username="two", email="two@two.com", password="my_password")

    default_user.role = admin_role
    second_user.role = user_role

    db.session.add(default_user)
    db.session.add(second_user)

    db.session.commit()
    # Commit the changes for the users
