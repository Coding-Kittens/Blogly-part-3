
from unittest import TestCase

from flask import *
from models import *
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()



class test_app(TestCase):

    def setUp(self):
        """gets rid of any users """
        Post.query.delete()
        User.query.delete()


    def tearDown(self):
        """clears db session """
        db.session.rollback()

    def test_show_users(self):
        """ Tests if all users show up on the users page """
        with app.test_client() as client:
            nick = User(first_name='nick',last_name='powell')
            larry = User(first_name='larry',last_name='powell')
            rose = User(first_name='rose',last_name='powell')

            db.session.add(rose)
            db.session.add(larry)
            db.session.add(nick)
            db.session.commit()

            res = client.get('/',follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn("nick powell",html)
            self.assertIn("rose powell",html)
            self.assertIn("larry powell",html)


    def test_make_new_user(self):
        """ Tests if a new user is added """
        with app.test_client() as client:
            res = client.post('/users/new',data={'first_name':'crystal','last_name':'powell','pic':''},follow_redirects=True)
            html = res.get_data(as_text = True)
            self.assertIn("crystal powell",html)



    def test_user_page(self):
        """ Tests that the right user is shown on the user page """
        with app.test_client() as client:
            rose = User(first_name='rose',last_name='powell')

            db.session.add(rose)
            db.session.commit()

            res = client.get(f'/user/{rose.id}')
            html = res.get_data(as_text=True)
            self.assertIn("rose powell",html)
            self.assertIn("Edit",html)
            self.assertIn("Delete",html)


    def test_delete_user(self):
        """ Tests if a user is deleted """
        with app.test_client() as client:
            rose = User(first_name='rose',last_name='powell')

            db.session.add(rose)
            db.session.commit()

            res = client.get(f'users/{rose.id}/delete',follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertNotIn("rose powell",html)


    def test_post_page(self):
        """ Tests that the right post is shown """
        with app.test_client() as client:

            rose = User(first_name='rose',last_name='powell')
            db.session.add(rose)
            db.session.commit()


            new_post = Post(title='testPost',content='this is a test post',user_id=rose.id)

            db.session.add(new_post)
            db.session.commit()

            res = client.get(f'/posts/{new_post.id}')
            html = res.get_data(as_text=True)
            self.assertIn("testPost",html)
            self.assertIn("this is a test post",html)
            self.assertIn(new_post.user.get_full_name(),html)
            self.assertIn("Back",html)
            self.assertIn("Edit",html)
            self.assertIn("Delete",html)



    def test_add_post(self):
        """ Tests if a new post is added """
        with app.test_client() as client:
            rose = User(first_name='rose',last_name='powell')
            db.session.add(rose)
            db.session.commit()
            res = client.post(f'/users/{rose.id}/posts/new',data={'title':'test2','content':'this is also a test'},follow_redirects=True)
            html = res.get_data(as_text = True)
            self.assertIn("test2",html)




    def test_edit_post(self):
            """ Tests if a post is edited """
            with app.test_client() as client:
                rose = User(first_name='rose',last_name='powell')
                db.session.add(rose)
                db.session.commit()


                new_post = Post(title='testPost',content='this is a test post',user_id=rose.id)
                db.session.add(new_post)
                db.session.commit()


                res = client.post(f'/posts/{new_post.id}/edit',data={'title':'testPost','content':'this is an edited post'},follow_redirects=True)
                html = res.get_data(as_text = True)
                self.assertIn("this is an edited post",html)
