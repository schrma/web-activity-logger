from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from activity_logger.blog_posts.forms import BlogPostForm
from activity_logger.models import BlogPost, db

blog_posts = Blueprint("blog_posts", __name__)


@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post_entry = BlogPost(
            title=form.title.data, text=form.text.data, user_id=current_user.id
        )
        db.session.add(blog_post_entry)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post_entry = BlogPost.query.get_or_404(blog_post_id)
    return render_template(
        "blog_post.html",
        title=blog_post_entry.title,
        date=blog_post_entry.date,
        post=blog_post_entry,
    )


@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    blog_post_entry = BlogPost.query.get_or_404(blog_post_id)
    if blog_post_entry.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post_entry.title = form.title.data
        blog_post_entry.text = form.text.data
        db.session.commit()
        flash("Post Updated")
        return redirect(url_for("blog_posts.blog_post", blog_post_id=blog_post_entry.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    if request.method == "GET":
        form.title.data = blog_post_entry.title
        form.text.data = blog_post_entry.text
    return render_template("create_post.html", title="Update", form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=["POST"])
@login_required
def delete_post(blog_post_id):
    blog_post_entry = BlogPost.query.get_or_404(blog_post_id)
    if blog_post_entry.author != current_user:
        abort(403)
    db.session.delete(blog_post_entry)
    db.session.commit()
    flash("Post has been deleted")
    return redirect(url_for("core.index"))
