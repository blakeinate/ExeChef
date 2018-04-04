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

    def test_account_creation_correct_info(self):
        #test account creation for correct info
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': username, 'password':'somepassword', 'email': username+'@gmail.com'})
        self.assertEqual(response.status_code, 200)

    def test_account_creation_username_in_use(self):
        #makes sure catches if username already in use
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': 'testusername', 'password': 'somepassword', 'email': email_name})
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': 'testusername', 'password': 'somepassword', 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_account_creation_email_in_use(self):
        #catch if email already in use
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testusername', 'password': 'somepassword', 'email': email_name})
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': username, 'password': 'somepassword', 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_account_creation_no_username(self):
        #catch no username provided
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/CreateAccount', json={'password': 'somepassword', 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_account_creation_no_password(self):
        #catch no password provided
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        email_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': username, 'email': email_name})
        self.assertEqual(response.status_code, 422)

    def test_account_creation_no_email(self):
        #catch no email provided
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        response = requests.post('http://localhost:5000/CreateAccount', json={'username': username, 'password': 'somepassword'})
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_correct_info(self):
        #test valid creation
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 201)

    def test_recipe_creation_no_name(self):
        #catch no recipe name
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_private(self):
        #catch no private
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_ingredients(self):
        #catch no ingredients
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)

    def test_recipe_creation_no_steps(self):
        #catch no steps
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                 }
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        self.assertEqual(response.status_code, 422)


class TestDataAccess(unittest.TestCase):
    def test_current_account_retrieval(self):
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/Account', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_public_recipe_retrieval_by_id(self):
        #test recipe retrieval for public recipe
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'False',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        recipe_id = response.json().get('data').get('id')
        response = requests.get('http://localhost:5000/Recipes/'+str(recipe_id))
        self.assertEqual(response.status_code, 200)

    def test_private_recipe_retrieval_invalid_permissions(self):
        #check that private recipe cannot be viewed without authorization
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        recipe_id = response.json().get('data').get('id')
        response = requests.get('http://localhost:5000/Recipes/'+str(recipe_id))
        self.assertEqual(response.status_code, 403)

    def test_private_recipe_valid_permissions(self):
        #if you private recipe and creator should be able to view
        requests.post('http://localhost:5000/CreateAccount', json={'username': 'testuser', 'password':'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login', json={'login': 'testuser', 'password':'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit':'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        recipe_id = response.json().get('data').get('id')
        response = requests.get('http://localhost:5000/Recipes/'+str(recipe_id), headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_invalid_id(self):
        #check response for non real recipe id
        response = requests.get('http://localhost:5000/Recipes/meepmooper')
        self.assertEqual(response.status_code, 500)

    def test_recipe_retrieval_by_user_favorites(self):
        #get valid account favorites
        requests.post('http://localhost:5000/CreateAccount',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/Favorites', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_retrieval_by_user_created(self):
        #get valid user recipes
        requests.post('http://localhost:5000/CreateAccount',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        header = {'Authorization': 'Bearer ' + str(access_token)}
        response = requests.get('http://localhost:5000/UserRecipes', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_recipe_retrieval_by_tags(self):
        #test correct retrieval
        requests.post('http://localhost:5000/CreateAccount',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
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
        requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        response = requests.get('http://localhost:5000/SearchTags/'+tag1 + ',' + tag2)
        recipes = response.json().get('data').get('recipes')
        self.assertEqual(True, (recipes != None))

    def test_private_recipe_retrieval_by_tags(self):
        #test that retrieval of private recipes does not occur
        requests.post('http://localhost:5000/CreateAccount',
                      json={'username': 'testuser', 'password': 'somepassword', 'email': 'testuser@gmail.com'})
        login_response = requests.post('http://localhost:5000/Login',
                                       json={'login': 'testuser', 'password': 'somepassword'})
        access_token = login_response.json().get('data').get('access_token')
        tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        recipe = {'name': 'testrecipe',
                  'private': 'True',
                  'tags': [tag],
                  'ingredients': [
                      {'name': 'someingredient',
                       'amount': '100', 'unit': 'pounds'}],
                  'steps': ['do cool stuff', 'do more stuff']}
        header = {'Authorization': 'Bearer ' + str(access_token)}
        requests.post('http://localhost:5000/CreateRecipe', json=recipe, headers=header)
        response = requests.get('http://localhost:5000/SearchTags/'+tag)
        recipes = response.json().get('data').get('recipes')
        self.assertEqual(recipes, None)

if __name__ == "__main__":
    unittest.main()