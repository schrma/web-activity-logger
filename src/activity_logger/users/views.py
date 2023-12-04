from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from activity_logger.models.db_activites import Activities, ActivityType, UnitType
from activity_logger.models.org import BlogPost, Role, User, db
from activity_logger.users.forms import (
    ActivityForm,
    LoginForm,
    RegistrationForm,
    UpdateUserForm,
)
from activity_logger.users.picture_handler import add_profile_pic

users_blueprint = Blueprint("users", __name__)


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or str(current_user.role) != "Admin":
            abort(403)  # HTTP status code for Forbidden
        return view_func(*args, **kwargs)

    return decorated_view


@users_blueprint.route("/register", methods=["GET", "POST"])
@login_required
@admin_required
def register():
    form = RegistrationForm()

    form.role.choices = [(role.id, role.role) for role in Role.query.all()]

    if form.validate_on_submit():
        user = User(
            email=form.email.data, username=form.username.data, password=form.password.data
        )
        # user.role = Role.query.filter_by(role="Admin").first()
        user.role = Role.query.filter_by(id=form.role.data).first()
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering! Now you can login!")
        return redirect(url_for("users.login"))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in field "{getattr(form, field).label.text}": {error}', "error")
    return render_template("register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash("User is not available", "error")
            return render_template("login.html", form=form)

        if not user.check_password(form.password.data):
            flash("Password is not correct", "error")
            return render_template("login.html", form=form)

        # Log in the user

        login_user(user, remember=True)

        flash("Logged in successfully.")

        # If a user was trying to visit a page that requires a login
        # flask saves that URL as 'next'.
        next = request.args.get("next")  # pylint: disable=redefined-builtin

        # So let's now check if that next exists, otherwise we'll go to
        # the welcome page.
        if next is None or not next[0] == "/":
            next = url_for("core.index")

        return redirect(next)
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in field "{getattr(form, field).label.text}": {error}', "error")

    return render_template("login.html", form=form)


@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users_blueprint.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            print("Picture available")
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("User Account Updated")
        print("User Account Updated")
        return redirect(url_for("users.account"))

    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for("static", filename="profile_pics/" + current_user.profile_image)
    return render_template("account.html", profile_image=profile_image, form=form)


@users_blueprint.route("/test/<username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = (
        BlogPost.query.filter_by(author=user)
        .order_by(BlogPost.date.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_blog_posts.html", blog_posts=blog_posts, user=user)


# Define the route for the home page
@users_blueprint.route("/activities", methods=["GET", "POST"])
def activities():
    # Create an instance of the form
    form = ActivityForm()

    form.activity.choices = [
        (activity.id, activity.activity_type) for activity in ActivityType.query.all()
    ]
    form.unit.choices = [(unit.id, unit.unit_type) for unit in UnitType.query.all()]

    # Check if the form is validated on submission
    if form.validate_on_submit():
        # Get the data from the form fields
        activity = form.activity.data
        time = form.time.data
        value = form.value.data
        unit = form.unit.data

        my_unit = UnitType.query.filter_by(id=unit).first()
        my_activity = ActivityType.query.filter_by(id=activity).first()

        activity_to_save = Activities(
            my_activity=my_activity, value=value, my_unit=my_unit, my_user=current_user
        )

        db.session.add(activity_to_save)
        db.session.commit()
        # Redirect to the result page with the data as query parameters
        return redirect(
            url_for("users.result", activity=activity, time=time, value=value, unit=unit)
        )
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in field "{getattr(form, field).label.text}": {error}', "error")
    # Render the template with the form as an argument
    return render_template("activities.html", form=form)


# Define the route for the result page
@users_blueprint.route("/result", methods=["GET", "POST"])
def result():
    # Get the data from the query parameters
    activity = request.args.get("activity")
    time = request.args.get("time")
    value = request.args.get("value")
    unit = request.args.get("unit")
    # Render the template with the data as arguments
    return render_template("result.html", activity=activity, time=time, value=value, unit=unit)


@users_blueprint.route("/flash", methods=["GET", "POST"])
def my_flash():
    # Defined in base.html (Flash)
    flash("Should be an error", "error")
    flash("Should be an info")
    return redirect(url_for("core.index"))
