"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()



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
    return render_template('user.html', user=user)


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

