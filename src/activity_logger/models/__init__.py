from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class BaseAdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and str(current_user.role) == "Admin"

    def inaccessible_callback(self, name, **kwargs):
        # Redirect unauthorized users to the login page
        return redirect(url_for("users.login"))


class BaseUserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect unauthorized users to the login page
        return redirect(url_for("users.login"))
