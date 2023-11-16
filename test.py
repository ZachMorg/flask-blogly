from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()



class BloglyTests(TestCase):


    def startUp(self):
        User.query.delete()
        Post.query.delete()
        user = User(first_name='Test', last_name='User', image_url='')
        post = Post(title='TEST', context='test', user_id=1)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()
        
        self.user_id = user.id
        self.post_id = post.id

        
    def test_index(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertIn('<h1>Blogly!</h1>', html)
            self.assertIn('<h2>Users:</h2>', html)
            


    def test_user(self):
        with app.test_client() as client:
            response = client.get(f'/users/1')
            html = response.get_data(as_text=True)

            self.assertIn('<button>Edit User</button>', html)
            self.assertIn('<li>', html)


    def test_edit(self):
        with app.test_client() as client:
            response = client.get(f'/users/1/edit')
            html = response.get_data(as_text=True)

            self.assertIn('<input name="first_name" value="">', html)


    def test_new(self):
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertIn('<input name="first_name">', html)