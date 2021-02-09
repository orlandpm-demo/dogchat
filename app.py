from flask import Flask, render_template, redirect, abort, request, url_for
from database import get_all_posts, get_dog_by_handle, get_posts_by_handle, insert_post, delete_post
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="templates", static_url_path='/static')
auth = HTTPBasicAuth()

users = {
    "melba": generate_password_hash("melba"),
    "rose": generate_password_hash("rose"),
    "chucky": generate_password_hash("chucky")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/feed')
@auth.login_required
def feed():
    posts = get_all_posts()
    print(posts)
    return render_template('feed.html', posts=posts, user=auth.current_user())


@app.route('/dog/<string:handle>')
@auth.login_required
def dog(handle):
    dog = get_dog_by_handle(handle)
    posts = get_posts_by_handle(handle)
    return render_template('dog.html', dog=dog, posts=posts)

@app.route('/create', methods = ['POST'])
@auth.login_required
def create():
    post_content = request.form['post-content']
    insert_post(auth.current_user(), post_content)
    return redirect(url_for('feed'))

@app.route('/delete')
@auth.login_required
def delete():
    post_id = request.args.get('post_id')
    delete_post(post_id,auth.current_user())
    return redirect(url_for('feed'))

@app.route('/')
@auth.login_required(optional=True)
def splash():
    if auth.current_user():
        return redirect(url_for('feed'))
    else:
        return render_template('splash.html')

@app.route('/logout')
def logout():
    return render_template('splash.html'), 401



if __name__ == "__main__":
    app.run(debug=True)