import unittest
import requests
import string
import random
import app_testing as app
from flask_pymongo import PyMongo

#client = app.client
app.app.config['MONGO2_DBNAME'] = 'unit_test_db'
app.client = PyMongo(app.app, config_prefix='MONGO2')

class TestCreationMethods(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_user_creation_correct_info(self):
        #test account creation for correct info
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/User', json={'username': username, 'password':'somepassword', 'email': username+'@gmail.com'})
        self.assertEqual(response.status_code, 200)

    def test_user_creation_username_in_use(self):
        #makes sure catches if username already in use
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/User', json={'username': 'testusername', 'password': 'somepassword', 'email': email_name})
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/User', json={'username': 'testusername', 'password': 'somepassword', 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_user_creation_email_in_use(self):
        #catch if email already in use
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        requests.post('http://localhost:5000/User', json={'username': 'testusername', 'password': 'somepassword', 'email': 'meep@gmail.com'})
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/User', json={'username': username, 'password': 'somepassword', 'email': 'meep@gmail.com'})
        self.assertEqual(response.status_code, 422)

    def test_user_creation_no_username(self):
        #catch no username provided
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/User', json={'password': 'somepassword', 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_user_creation_no_password(self):
        #catch no password provided
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/User', json={'username': username, 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_user_creation_no_email(self):
        #catch no email provided
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/User', json={'username': username, 'password': 'somepassword'})
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_correct_info(self):
        #test valid creation
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe':
                      {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
                  }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 201)

    def test_recipe_creation_no_name(self):
        #catch no recipe name
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = { 'recipe':{
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_private(self):
        #catch no private
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_ingredients(self):
        #catch no ingredients
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'private': 'True',
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_steps(self):
        #catch no steps
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                 }
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_comment_creation_valid(self):
        # test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'recipe': {
            'name': 'testrecipe',
            'private': 'True',
            'tags': [tag],
            'ingredients': [
                {'name': 'someingredient',
                 'amount': '100', 'unit': 'pounds'}],
            'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        comment = {'comment': {'body': 'superdupercomment here'}}
        response = requests.post('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments', json=comment, headers=header)
        self.assertEqual(200, response.status_code)

    def test_comment_creation_invalid_no_text(self):
        # test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'recipe': {
            'name': 'testrecipe',
            'private': 'True',
            'tags': [tag],
            'ingredients': [
                {'name': 'someingredient',
                 'amount': '100', 'unit': 'pounds'}],
            'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        comment = {'comment': {'body': ''}}
        response = requests.post('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments', json=comment, headers=header)
        self.assertEqual(422, response.status_code)

class TestDataAccess(unittest.TestCase):
    def test_current_user_retrieval(self):
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/User', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_user_retrieval_no_sensitive_info(self):
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        response = requests.get('http://localhost:5000/User/testuser')
        self.assertEqual(response.status_code, 200)

    def test_other_user_retrieval_no_sensitive_info_with_access_token_for_current_user(self):
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        requests.post('http://localhost:5000/User', json={'username': 'testuser2', 'password':'somepassword', 'email': 'testuser2@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/User/testuser2', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_public_recipe_retrieval_by_id(self):
        #test recipe retrieval for public recipe
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'private': False,
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        response = requests.get('http://localhost:5000/Recipe/'+str(recipe_id))
        self.assertEqual(response.status_code, 200)

    def test_private_recipe_retrieval_invalid_permissions(self):
        #check that private recipe cannot be viewed without authorization
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'private': True,
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        response = requests.get('http://localhost:5000/Recipe/'+str(recipe_id))
        self.assertEqual(response.status_code, 403)

    def test_private_recipe_valid_permissions(self):
        #if you private recipe and creator should be able to view
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {
                  'recipe':{
                  'name': 'testrecipe',
                  'private': True,
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        response = requests.get('http://localhost:5000/Recipe/'+str(recipe_id), headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_invalid_id(self):
        #check response for non real recipe id
        response = requests.get('http://localhost:5000/Recipe/meepmooper')
        self.assertEqual(response.status_code, 500)

    def test_recipe_retrieval_by_user_favorites(self):
        #get valid account favorites
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/Recipe/Favorites/CurrentUser', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_retrieval_by_user_created(self):
        #get valid user recipes
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/Recipe/Created/CurrentUser', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_retrieval_by_tags(self):
        #test correct retrieval
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        tag2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        recipe = {
                  'recipe':{
                  'name': 'testrecipe',
                  'private': 'False',
                  'tags': [tag1, tag2],
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        response = requests.get('http://localhost:5000/SearchTags/'+tag1)
        recipes = response.json().get('recipes')
        self.assertEqual(True, (recipes != None))

    def test_private_recipe_retrieval_by_tags(self):
        #test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'recipe': {
                  'name': 'testrecipe',
                  'private': 'True',
                  'tags': [tag],
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        response = requests.get('http://localhost:5000/SearchTags/'+tag)
        check_empty = response.json().get('recipes')
        self.assertEqual(0, len(check_empty))

    def test_comment_retrieval(self):
        # test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'recipe': {
            'name': 'testrecipe',
            'private': 'True',
            'tags': [tag],
            'ingredients': [
                {'name': 'someingredient',
                 'amount': '100', 'unit': 'pounds'}],
            'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        comment = {'comment': {'body': 'superdupercomment here'}}
        requests.post('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments', json=comment, headers=header)
        response = requests.get('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments')
        length = len(response.json().get('comments'))
        self.assertEqual(True, length > 0)


class TestDataUpdating(unittest.TestCase):
    def test_user_update_bio_email_valid_info(self):
        email_name = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com')
        bio = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'bio': bio,
             'email': email_name,
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        good_update = False
        user = response.json().get('user')
        if (user.get('bio') == bio) and (user.get('email') == email_name):
            good_update = True
        self.assertEqual(True, good_update)

    def test_user_update_followers_follow_unfollow_valid_info(self):
        user_to_follow = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        user_to_update = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        #create user to follow
        requests.post('http://localhost:5000/User',
                      json={'username': user_to_follow, 'password': 'somepassword', 'email': user_to_follow+'@gmail.com'})
        #create user to update
        requests.post('http://localhost:5000/User',
                      json={'username': user_to_update, 'password': 'somepassword', 'email': user_to_update+'@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': user_to_update, 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'following': [user_to_follow]
         }
        #update followed list of user
        update_response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        followed_user = requests.get('http://localhost:5000/User/'+user_to_follow,  headers=header)
        user = update_response.json().get('user')
        followed_user = followed_user.json().get('user')
        #check that updates were successful for both updated user's following list
        #as well as followed_user's followers list
        good_update = False
        if (user_to_follow in user.get('following')) and (user_to_update in followed_user.get('followers')):
            good_update = True
        self.assertEqual(True, good_update)

        #now test unfollow and followers removal
        to_update = {
             'following': []
         }
        update_response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        followed_user = requests.get('http://localhost:5000/User/'+user_to_follow,  headers=header)
        user = update_response.json().get('user')
        followed_user = followed_user.json().get('user')
        # check that updates were successful for both updated user's following list
        # as well as followed_user's followers list
        good_update = False
        if (user_to_follow not in user.get('following')) and (user_to_update not in followed_user.get('followers')):
            good_update = True
        self.assertEqual(True, good_update)

    def test_user_update_favorites_valid_info(self):
        email_name = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com')
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'favorites': []
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        self.assertEqual(200, response.status_code)

    def test_user_update_password_valid_info(self):
        username = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        requests.post('http://localhost:5000/User',
                      json={'username': username, 'password': 'somepassword', 'email': username+'@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': username, 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'old_password': 'somepassword',
             'new_password': 'somenewpassword'
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        self.assertEqual(200, response.status_code)



    def test_user_update_password_invalid_info(self):
        #first test old password incorrect
        username = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        requests.post('http://localhost:5000/User',
                      json={'username': username, 'password': 'somepassword', 'email': username+'@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': username, 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'old_password': 'somepassword2',
             'new_password': 'somenewpassword'
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        self.assertEqual(422, response.status_code)
        #now test is only one of the password fields provided
        to_update = {
             'old_password': 'somepassword',
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        self.assertEqual(422, response.status_code)
        to_update = {
             'new_password': 'somenewpassword'
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)
        self.assertEqual(422, response.status_code)

    def test_user_update_bio_email_invalid_info(self):
        #create invalid email name (i.e. with no @email.something
        email_name = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        bio = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_update = {
             'bio': bio,
             'email': email_name,
         }
        response = requests.put('http://localhost:5000/User', json=to_update, headers=header)

        self.assertEqual(422, response.status_code)

    def test_user_update_anything_no_access_token(self):
        #create invalid email name (i.e. with no @email.something
        bio = str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        to_update = {
             'bio': bio,
         }
        response = requests.put('http://localhost:5000/User', json=to_update)

        self.assertEqual(401, response.status_code)

    def test_recipe_update_valid(self):
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_create = {
            'recipe':{
                'name': 'somenamehere',
                'tags': ['dankness', 'goodfood'],
                'steps': [
                  'heat oven',
                  'put food in',
                  'eat the food'
                ],
                'private':'True',
                'ingredients': [
                    {
                        'amount': 'tree-fitty',
                        'name': 'dank',
                        'unit': 'pounds'
                    }
                ]
            }
        }
        response = requests.post('http://localhost:5000/Recipe', json=to_create, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        to_update = {
            'recipe': {
                'id': str(recipe_id),
                'name': 'somenamehere',
                'tags': ['dankness', 'goodfood', 'meepmoooperr'],
                'steps': [
                  'heat oven',
                  'eat the food'
                ],
                'private':'True',
                'ingredients': [
                    {
                        'amount': 'tree-forty',
                        'name': 'daneek',
                        'unit': 'pounds'
                    }
                ]
                }
        }
        response = requests.put('http://localhost:5000/Recipe', json=to_update, headers=header)
        self.assertEqual(200, response.status_code)

    def test_recipe_update_invalid(self):
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_create = {'recipe': {
            'name': 'somenamehere',
            'tags': ['dankness', 'goodfood'],
            'steps': [
              'heat oven',
              'put food in',
              'eat the food'
            ],
            'private':'True',
            'ingredients': [
                {
                    'amount': 'tree-fitty',
                    'name': 'dank',
                    'unit': 'pounds'
                }
            ]
        }
        }
        response = requests.post('http://localhost:5000/Recipe', json=to_create, headers=header)
        to_update = {
            'recipe': {
            'name': 'somenamehere',
            'tags': ['dankness', 'goodfood', 'meepmoooperr'],
            }
        }
        response = requests.put('http://localhost:5000/Recipe', json=to_update, headers=header)
        self.assertEqual(422, response.status_code)

class TestDataDeletion(unittest.TestCase):
    #test recipe deletion, does not check if recipe ID removed from other users favorites
    def test_recipe_deletion_general(self):
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        to_create = {
            'recipe': {
                'name': 'somenamehere',
                'tags': ['dankness', 'goodfood'],
                'steps': [
                  'heat oven',
                  'put food in',
                  'eat the food'
                ],
                'private':'True',
                'ingredients': [
                    {
                        'amount': 'tree-fitty',
                        'name': 'dank',
                        'unit': 'pounds'
                    }
                ]
            }
        }
        response = requests.post('http://localhost:5000/Recipe', json=to_create, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        response = requests.delete('http://localhost:5000/Recipe/'+str(recipe_id), headers=header)
        self.assertEqual(200, response.status_code)

    def test_recipe_deletion_check_other_user_favorites(self):
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser2', 'password': 'somepassword', 'email': 'testuser2@gmail.com'})
        login_response2 = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser2', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        access_token2 = login_response2.json().get('user').get('access_token')

        header = {'Authorization': 'Bearer ' + str(access_token)}
        header2 = {'Authorization': 'Bearer ' + str(access_token2)}

        to_create = {
            'recipe': {
                'name': 'somenamehere',
                'tags': ['dankness', 'goodfood'],
                'steps': [
                  'heat oven',
                  'put food in',
                  'eat the food'
                ],
                'private':'True',
                'ingredients': [
                    {
                        'amount': 'tree-fitty',
                        'name': 'dank',
                        'unit': 'pounds'
                    }
                ]
            }
        }
        response = requests.post('http://localhost:5000/Recipe', json=to_create, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        to_update = {
            'favorites': [str(recipe_id)]
        }
        requests.put('http://localhost:5000/User', json=to_update, headers=header2)

        response = requests.delete('http://localhost:5000/Recipe/'+str(recipe_id), headers=header)

        favorited_user_response = requests.get('http://localhost:5000/User', headers=header2)

        found = True
        if favorited_user_response.json().get('favorites'):
            if str(recipe_id) not in favorited_user_response.json().get('favorites'):
                found = False
        else:
            found = False

        self.assertEqual(False, found)


    def test_comment_deletion(self):
        # test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'recipe': {
            'name': 'testrecipe',
            'private': 'True',
            'tags': [tag],
            'ingredients': [
                {'name': 'someingredient',
                 'amount': '100', 'unit': 'pounds'}],
            'steps': ['do cool stuff', 'do more stuff']}
        }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('recipe').get('_id').get('$oid')
        comment = {'comment': {'body': 'superdupercomment here'}}
        response = requests.post('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments', json=comment, headers=header)
        comment_id = response.json().get('comment').get('_id').get('$oid')
        response = requests.get('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments')
        length_old = len(response.json().get('comments'))
        requests.delete('http://localhost:5000/Recipe/comments/'+str(comment_id), headers=header)
        response = requests.get('http://localhost:5000/Recipe/' + str(recipe_id) + '/comments')
        length_new = len(response.json().get('comments'))
        self.assertEqual(True, length_new < length_old)


if __name__ == "__main__":
    unittest.main()