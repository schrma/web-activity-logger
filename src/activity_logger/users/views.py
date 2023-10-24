from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from activity_logger.models.org import BlogPost, User, db
from activity_logger.users.forms import LoginForm, RegistrationForm, UpdateUserForm, ActivityForm
from activity_logger.users.picture_handler import add_profile_pic

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data, username=form.username.data, password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering! Now you can login!")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            # Log in the user

            login_user(user)
            flash("Logged in successfully.")

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get("next")  # pylint: disable=redefined-builtin

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next is None or not next[0] == "/":
                next = url_for("core.index")

            return redirect(next)
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
@users_blueprint.route('/activities', methods=['GET', 'POST'])
def activities():
    # Create an instance of the form
    form = ActivityForm()
    # Check if the form is validated on submission
    if form.validate_on_submit():
        # Get the data from the form fields
        activity = form.activity.data
        time = form.time.data
        value = form.value.data
        unit = form.unit.data
        # Redirect to the result page with the data as query parameters
        return redirect(url_for('users.result', activity=activity, time=time, value=value, unit=unit))
    # Render the template with the form as an argument
    return render_template('activities.html', form=form)

# Define the route for the result page
@users_blueprint.route('/result',  methods=['GET', 'POST'])
def result():
    # Get the data from the query parameters
    activity = request.args.get('activity')
    time = request.args.get('time')
    value = request.args.get('value')
    unit = request.args.get('unit')
    # Render the template with the data as arguments
    return render_template('result.html', activity=activity, time=time, value=value, unit=unit)
