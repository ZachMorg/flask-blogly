"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()


# USER ROUTES -------------------------------------------------

@app.route('/')
def redirect_to_users():

    return redirect('/users')


@app.route('/users')
def list_users():

    print(User.query.all())
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/users/new')
def show_new_form():

    return render_template('form.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    print(image_url)

    user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get(user_id)
    print(user)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template('user.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):

    user = User.query.get(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# POST ROUTES -------------------------------------------------


@app.route('/users/<int:user_id>/posts/new')
def show_new_post(user_id):

    tags = Tag.query.all()

    return render_template('new_post.html', user_id=user_id, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):

    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tags')
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):

    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tags = request.form.getlist('tags')
    post.tags = Tag.query.filter(Tag.id.in_(tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


# TAG ROUTES --------------------------------------------------


@app.route('/tags')
def show_tags():

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new')
def new_tag_form():

    return render_template('new_tag.html')


@app.route('/tags/new', methods=['POST'])
def add_new_tag():

    title = request.form['title']
    tag = Tag(title=title)

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):

    tag = Tag.query.get(tag_id)
    posts = Post.query.all()
    return render_template('tag_detail.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit(tag_id):

    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):

    tag = Tag.query.get(tag_id)
    tag.title = request.form['title']

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')