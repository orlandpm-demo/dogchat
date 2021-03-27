import flask
from flask import Flask, render_template, redirect, abort, request, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FileField
from database import get_all_posts, get_dog_by_handle, get_posts_by_handle, insert_post, delete_post, create_user, make_avatar_url, like_post, unlike_post, like_count, toggle_like, get_comments
# from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import secrets
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import dog_email
import json

app = Flask(__name__, template_folder="templates", static_url_path='/static')

login_manager = LoginManager()

login_manager.init_app(app)

# users = {
#     "melba": generate_password_hash("MelbaMelba123$$$"),
#     "rose": generate_password_hash("rose"),
#     "chucky": generate_password_hash("chucky")
# }

app.secret_key = b'ams,hjdfiouqjh20f9ajsdifja0-923hjr0'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User():
    def __init__(self, username):
        dog = get_dog_by_handle(username)
        self.username = username
        self.avatar_image_name = dog['AvatarImageName']

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def get(cls,username):
        return User(username)

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and \
#             check_password_hash(users.get(username), password):
#         return username

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('Username')
    name = StringField('Name')
    bio = TextAreaField('Bio')
    age = IntegerField('Age')
    avatar = FileField('Avatar')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route("/reset-password", methods = ['POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        dog_email.reset_password(username)
        return 'password successfully reset, check your email'
    else:
        return 'failed to reset password, try again!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    reset_password_form = ResetPasswordForm()
    if form.validate_on_submit():
        # Login and validate the user.

        username = form.username.data
        password = form.password.data

        dog = get_dog_by_handle(username)

        if dog and \
            check_password_hash(dog['PasswordHash'], password):

            user = User(username)
        # user should be an instance of your `User` class
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('splash'))
    return flask.render_template('login.html', form=form, reset_password_form=reset_password_form)


@app.route('/test')
@login_required
def test():
    return render_template('test.html')

# @app.route('/dog/<string:handle>')
# @login_required
# def dog(handle):
#     dog = get_dog_by_handle(handle)
#     posts = get_posts_by_handle(handle)
#     return render_template('dog.html', dog=dog, posts=posts)

@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    username = current_user.username
    like_result = toggle_like(username, post_id)
    print('like count came back as:', like_result)
    return json.dumps(like_result)

@app.route('/api/comments/<int:post_id>')
@login_required
def comments_api(post_id):
    c = get_comments(post_id)
    return json.dumps(c, indent=4)

@app.route('/api/feed')
@login_required
def feed_api():
    username = current_user.username
    posts = get_all_posts(username)
    return json.dumps(posts, indent=4)

@app.route('/api/dog/<string:handle>')
@login_required
def dog_api(handle):
    dog = get_dog_by_handle(handle)
    posts = get_posts_by_handle(handle)
    data = {
        'dog':dog,
        'posts':posts
    }
    return json.dumps(data, indent=4)

# def feed():
#     username = current_user.username
#     posts = get_all_posts(username)
#     my_avatar_url = make_avatar_url(current_user.avatar_image_name)
#     return render_template('feed.html', posts=posts, user=username, my_avatar_url=my_avatar_url)



# @app.route('/delete')
# @login_required
# def delete():
#     post_id = request.args.get('post_id')
#     delete_post(post_id,current_user.username)
#     return redirect(url_for('feed'))

@app.route('/')
@login_required
def splash():
    # if auth.current_user():
        return render_template('base.html', username=current_user.username)
    # else:
    #     return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password_hash = generate_password_hash(form.password.data)
        bio = form.bio.data
        age = form.age.data
        name = form.name.data
        avatar = form.avatar.data

        print(avatar)
        print(avatar.filename)

        blob_service_client = BlobServiceClient.from_connection_string(secrets.blob_connection_string)
        blob_client = blob_service_client.get_blob_client(container=secrets.container_name, blob=avatar.filename)
        blob_client.upload_blob(avatar)
        # validate 
        # * not existing username
        # * username/password are valid (not empty strings)
        
        create_user(username, name, bio, age, password_hash, avatar.filename)

    

        user = User(username)
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('splash'))
    return render_template('signup.html',form=form)

# @app.route('/logout')
# @login_required
# def logout():
#     return render_template('splash.html'), 401

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('splash'))


if __name__ == "__main__":
    app.run(debug=True)