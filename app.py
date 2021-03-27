"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc 
from models import db, User, Post, Tag, PostTag, connect_db
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
    posts = Post.query.order_by(desc(Post.created_at))[:5]
    return render_template('users.html', users=users, posts=posts)

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
 
@app.route('/users/<userid>', methods=['GET', 'POST'])
def show_user_page(userid):
    """Show data about a specific user"""
    user = User.query.get(userid)
    posts = user.posts
    tags = [post.tags for post in posts]
    return render_template('user-overview-page.html', user=user, posts=posts, tags=tags)

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
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<userid>/posts/new', methods=["POST"])
def handle_new_post(userid):
    """Add post and redirect to the user detail page"""
    tag_ids = [int(num) for num in request.form.getlist("tag_checkbox")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=request.form['post_title'], content=request.form['post_content'], posted_by=userid, tags=tags)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('show_user_page', userid=userid))

@app.route('/posts/<postid>')
def show_post(postid):
    #template for this is missing
    """Show a post"""
    post = Post.query.get(postid)
    return render_template('new_post', post=post)

@app.route('/posts/<postid>/edit')
def show_edit_post_form(postid):
    """Show form to edit a post"""
    post = Post.query.get(postid)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<postid>/edit', methods=['POST'])
def handle_edit_post(postid):
    """Handle editing of a post - redirect back to the post view"""
    post = Post.query.get(postid)
    post.title = request.form['post_title']
    post.content = request.form['post_content']
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('show_user_page', userid=post.posted_by))

@app.route('/posts/<postid>/delete')
def handle_delete_post(postid):
    #grab user who created post, delete post, then redirect to user page
    post = Post.query.get(postid)
    userid = post.posted_by
    db.session.delete(post)
    db.session.commit() 
    return redirect(url_for('show_user_page', userid=userid))

@app.route('/tags')
def show_all_tags():
    """lists all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    posts = Post.query.all()
    return render_template('tags.html', tags=tags, posts=posts)
    
@app.route('/tags/new')
def show_add_tag():
    """Shows a form to add a new tag"""
    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def handle_add_tag():
    """Process addition of new tag and redirect to tag list"""
    new_tag = Tag(name=request.form['tag-name'])
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('show_all_tags'))

@app.route('/tags/<tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get(tag_id)
    return render_template('tag_edit_form.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_edit_tag_form(tag_id):
    """Process edit form, edit tag and redirect to the tags list"""
    tag = Tag.query.get(tag_id)
    tag.name = request.form['tag-name']
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('show_all_tags'))

@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('show_all_tags'))
