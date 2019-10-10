from flask import render_template, request, redirect, url_for, flash, abort

from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin

from app import app, db
from datetime import date, time, datetime

from models import User, Post
from hashutils import check_pw_hash


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

now = datetime.now()
current_year = now.strftime("%Y")
current_day = now.strftime("%a %B %d, %Y")
current_time = now.strftime("%X")

##### Nav_bar sign in and signout color  ###################

color_signIn = "bg-danger"
color_signOut = "bg-dark"

##############################

## Create Global Variables ###
@app.context_processor
def context_processor():
    return dict(current_year=current_year, current_day=current_day, current_time=current_time, color_signIn=color_signIn, color_signOut=color_signOut)


# Check enpoint before loading view
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('display_blogs'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_pw_hash(password, user.pw_hash):
            login_user(user)
            flash('Logged in Success!', 'success')
            return redirect(url_for('display_blogs'))
        else:
            flash('Login Unsuccessfully. Please check email and password', 'danger')

    return render_template('login.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('display_blogs'))
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password-confirm']
        username_error = ''
        email_error = ''
        password_error = ''
        confirm_password_error = ''

        # Username validation

        if username == '':
            username_error = "Username cannot be left empty"
        elif len(username) < 3:
            username_error = "Username cannot be less than 3 characters"
        elif len(username) > 20:
            username_error = "Username cannot be more than 20 characters"
        elif ' ' in username:
            username_error = "Username contains space"
        # End of Username validation

        # Email validation

        if email == '':
            email_error = "Email cannot be left empty"
        elif "@" not in email:
            email_error = "Email does not have '@'"
        elif "." not in email:
            email_error = "email does not contain any '. (Period)'"
        elif ' ' in email:
            email_error = "email contains space"
        elif len(email) < 3:
            username_error = "Email cannot have less than 3 characters"
        elif len(email) > 20:
            username_error = "Email cannot have more than 20 characters"
        # End of Email validation

        # Password validation

        if password == '':
            password_error = "Password field cannot be left empty"
        elif len(password) < 3:
            password_error = "Password cannot be less than 3 characters"
        elif len(password) > 20:
            password_error = "Password cannot be more than 20 characters"
        elif ' ' in password:
            password_error = "Password contains space"
        if not password_error:
            if confirm_password == '':
                confirm_password_error = "Please Confirm your password"
            elif confirm_password != password:
                confirm_password_error = "Password does not match"
        # End of Password validation

        if not username_error and not email_error and not password_error and not confirm_password_error:
            existing_email = User.query.filter_by(email=email).first()
            existing_username = User.query.filter_by(username=username).first()
            if not existing_email and not existing_username:
                new_user = User(email, username, password)
                db.session.add(new_user)
                db.session.commit()
                flash(
                    f'Account has been created! Thank you {username}!', 'success')
                return redirect(url_for('login'))
            else:
                flash(
                    'Username or email taken. Please choose another one', 'danger')
                return redirect(url_for('signup'))
        else:
            return render_template('signup.html', username_error=username_error, email_error=email_error, password_error=password_error, confirm_password_error=confirm_password_error)
    else:
        return render_template('signup.html')


@app.route('/logout')
def logout():
    logout_user()
    flash("You logged out!", 'success')
    return redirect(url_for('display_blogs'))


@app.route("/blogs")
def display_blogs():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blogs.html', posts=posts)


@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def add_new_post():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        post_title_error = ''
        post_body_error = ''
        if post_title == '':
            post_title_error = "Title cannot be left empty"
        if post_body == '':
            post_body_error = "Please type your post Here!"
        if not post_title_error and not post_body_error:
            new_post = Post(post_title, post_body, owner=current_user)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('display_blogs'))
        else:
            return render_template('newpost.html', post_title_error=post_title_error, post_body_error=post_body_error)
    else:
        return render_template('newpost.html')


@app.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.owner != current_user:
        abort(403)
    if request.method == 'POST':
        post.post_title = request.form['title']
        post.post_body = request.form['body']
        db.session.commit()
        flash('Blog Post Updated', 'success')
        return redirect(url_for('single_post', post_id=post.id))
    elif request.method == 'GET':
        post_title = post.post_title
        post_body = post.post_body
    return render_template('newpost.html')


@app.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.owner != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('single_post'))

    db.session.delete(post)
    db.session.commit()
    flash('Blog Post Deleted', 'success')
    return redirect(url_for('display_blogs'))


@app.route("/post/<int:post_id>")
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('single-blog.html', post=post)


@app.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    post_number = Post.query.filter_by(owner=user).count()
    posts = Post.query.filter_by(owner=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user-blogs.html', posts=posts, user=user, post_number=post_number)


@app.route("/")
def users():
    page = request.args.get('page', 1, type=int)
    users_number = User.query.count()
    users = User.query.order_by(
        User.username.asc()).paginate(page=page, per_page=10)
    return render_template('index.html', users=users, users_number=users_number)


app.secret_key = '2d9b6941f4497350b2d8c7ae1321a312'

if __name__ == "__main__":
    app.run(debug=True)
