"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):

    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__='users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String,
                           nullable=False,
                           unique=False)

    last_name = db.Column(db.String,
                          nullable=False,
                          unique=False)

    image_url = db.Column(db.String,
                          nullable=False,
                          unique=False,
                          default='https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg')

    posts = db.relationship('Post', backref='user')
    

class Post(db.Model):

    __tablename__='posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String,
                      nullable=False)

    content = db.Column(db.String,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=True,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    tags = db.relationship('PostTag',
                             backref='post')

    
