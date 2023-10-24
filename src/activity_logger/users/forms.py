from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField, DateTimeLocalField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo

from activity_logger.models.org import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), EqualTo("pass_confirm", message="Passwords Must Match!")],
    )
    pass_confirm = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register!")

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is taken!")


class UpdateUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        # Check if not None for that user email!
        if user and user != current_user:
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and user != current_user:
            raise ValidationError("This username is taken.")


# Define the activities and units choices for the dropdown menus
activities = [('running', 'Running'), ('cycling', 'Cycling'), ('swimming', 'Swimming')]
units = [('km', 'Kilometers'), ('mi', 'Miles'), ('m', 'Meters')]

# Create a Flask-WTF form class
class ActivityForm(FlaskForm):
    # Dropdown menu with activities
    activity = SelectField('Choose an activity', choices=activities, validators=[DataRequired()])
    # Box to select time and date
    # time = DateTimeLocalField('Enter the time and date of your activity', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    time = DateTimeLocalField('Enter the time and date of your activity', format='%Y-%m-%dT%H:%M:%S', default=datetime.now)
    # Float field with values
    value = FloatField('Enter the distance or duration of your activity', validators=[DataRequired()])
    # Dropdown menu with different units
    unit = SelectField('Choose the unit of your value', choices=units, validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Submit')
