import unittest
import requests
import string
import random
import app
from pymongo import MongoClient

client = MongoClient()

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
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 201)

    def test_recipe_creation_no_name(self):
        #catch no recipe name
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_private(self):
        #catch no private
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_ingredients(self):
        #catch no ingredients
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_steps(self):
        #catch no steps
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                 }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)


class TestDataAccess(unittest.TestCase):
    def test_current_account_retrieval(self):
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/User', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_public_recipe_retrieval_by_id(self):
        #test recipe retrieval for public recipe
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'False',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('id')
        response = requests.get('http://localhost:5000/Recipe/'+str(recipe_id))
        self.assertEqual(response.status_code, 200)

    def test_private_recipe_retrieval_invalid_permissions(self):
        #check that private recipe cannot be viewed without authorization
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('id')
        response = requests.get('http://localhost:5000/Recipe/'+str(recipe_id))
        self.assertEqual(response.status_code, 403)

    def test_private_recipe_valid_permissions(self):
        #if you private recipe and creator should be able to view
        requests.post('http://localhost:5000/User', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        recipe_id = response.json().get('id')
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
        response = requests.get('http://localhost:5000/Favorites', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_retrieval_by_user_created(self):
        #get valid user recipes
        requests.post('http://localhost:5000/User',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('user').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/UserRecipes', headers=header)
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

        recipe = {'name': 'testrecipe',
                  'private': 'False',
                  'tags': [tag1, tag2],
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
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
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'tags': [tag],
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        requests.post('http://localhost:5000/Recipe', json=recipe, headers=header)
        response = requests.get('http://localhost:5000/SearchTags/'+tag)
        check_empty = response.json().get('recipes')
        self.assertEqual(0, len(check_empty))

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






if __name__ == "__main__":
    unittest.main()