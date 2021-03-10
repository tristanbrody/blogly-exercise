"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, User, Post, connect_db
from seed import seed

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
connect_db(app)

#run seed file with test data
seed() 

@app.route('/')
def home():
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_user():
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def handle_add_user():
    """Add a new user then redirect to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_image_url = request.form['profile_image_url']
    new_user = User(first_name=first_name, last_name=last_name, profile_image_url=profile_image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('list_users'))
 
@app.route('/users/<userid>')
def show_user_page(userid):
    """Show data about a specific user"""
    user = User.query.get(userid)
    posts = user.posts
    return render_template('user-overview-page.html', user=user, posts=posts)

@app.route('/users/<userid>/edit')
def show_user_edit_page(userid):
    """Edit a user"""
    user = User.query.get(userid)
    return render_template('user-edit-page.html', user=user)

@app.route('/users/<userid>/edit', methods=["POST"])
def handle_edit_user(userid):
    """Edit a user then redirect to /users"""
    user = User.query.get(userid)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.profile_image_url = request.form['profile_image_url']
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('list_users'))

@app.route('/users/<userid>/delete')
def handle_delete_user(userid):
    """Delete a user then redirect to /users"""
    User.query.filter_by(id=userid).delete()
    db.session.commit()
    return redirect(url_for('list_users'))

@app.route('/users/<userid>/posts/new')
def show_new_post_form(userid):
    """Show form to add a post for that user"""
    user = User.query.get(userid)
    return render_template('new_post.html', user=user)

@app.route('/users/<userid>/posts/new', methods=["POST"])
def handle_new_post(userid):
    """Add post and redirect to the user detail page"""
    user = User.query.get(userid)
    post = Post(title=request.form['post_title'], content=request.form['post_content'], posted_by=userid)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('show_user_page', userid=userid))

@app.route('/posts/<postid>')
def show_post(postid):
    """Show a post"""
    post = Post.query.get(postid)
    return render_template('new_post', post=post)

@app.route('/posts/<postid>/edit')
def show_edit_post_form(postid):
    """Show form to edit a post"""
    post = Post.query.get(postid)
    return render_template('edit_post', post=post)

@app.route('/posts/<postid>/edit', methods=['POST'])
def handle_edit_post(postid):
    """Handle editing of a post - redirect back to the post view"""
    post = Post.query.get(postid)
    return render_template('show_post', post=post)

@app.route('/posts/<postid>/delete')
def handle_delete_post(postid):
    #delete post
    return ''



