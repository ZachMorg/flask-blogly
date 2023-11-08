"""Models for Blogly."""

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
                          
                          
                          
                          
                          
