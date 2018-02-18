from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from flask import jsonify
from flask_jwt import JWT, jwt_required, current_identity
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from datetime import datetime
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

client = MongoClient()

class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id

class Accounts(Resource):
    def get(self):
        try:
            db = client.exechef
            cursor = db.accounts.find()
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'accounts': true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

class Account(Resource):
    @jwt_required()
    def get(self):
        try:
            _account_id = dict(current_identity).get('user_id')
            db = client.exechef
            cursor = db.accounts.find_one({'_id': ObjectId(_account_id)})
            if cursor == None:
                return jsonify({'error': 'account id invalid'})
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'account': true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

class Update_Password(Resource):
    def put(self):
        try:
            db = client.exechef
            json_data = request.get_json(force=True)

            _account_name = json_data['username']
            _old_password = json_data['old_password']
            _new_password = json_data['new_password']

            cursor = db.accounts.find_one({'username': _account_name})
            if cursor['password'] == _old_password:
                result = db.accounts.update_one(
                    {'username':_account_name},
                    {
                        '$set': {
                            'password': _new_password
                        }
                    }
                )
                if result.modified_count == 1:
                    return jsonify({'updated' : True})
                else:
                    return jsonify({'updated': False})
            else:
                return jsonify({'error': 'old password incorrect'})
        except Exception as e:
            return jsonify({'error': str(e)})

class Create_Account(Resource):
    def post(self):
        try:
            db = client.exechef
            json_data = request.get_json(force=True)
            _account_name = json_data['username']
            _account_password = json_data['password']

            #add password stuff here, encrypting and uploading

            #check if username exists
            cursor = db.accounts.find_one({'username': _account_name})
            if cursor != None:
                return jsonify({'error':'username taken'})

            #upload new account info to pymongo db
            result = db.accounts.insert_one(
            {
                'username': _account_name,
                'password': _account_password,
                'favorites': [],
                'created' : []
            })
            #return the id of the new account
            return jsonify({'created': True})
        except Exception as e:
            return jsonify({'error': str(e)})


#checks if a username and password match
def authenticate(username, password):
    try:
        _account_name = username
        _account_password = password
        db = client.exechef
        #add password getting, encrypting, and comparison
        cursor = db.accounts.find_one({'username': _account_name})
        if cursor == None:
            return False
        if cursor['password'] == _account_password:
            return User(id=str(cursor.get('_id')))
        else:
            return False
    except Exception as e:
        return False

#allows us to retrieve the user's id securely
def identity(payload):
    user_id = payload['identity']
    print payload, "PAYLOAD"
    return {'user_id':user_id}

class Favorites(Resource):
    @jwt_required()
    def get(self):
        try:
            db = client.exechef
            _account_id = dict(current_identity).get('user_id')
            #return list of recipes from user {'userFavorites': []}
            cursor = db.accounts.find_one({'_id': ObjectId(_account_id)})
            if cursor == None:
                return jsonify({'error': 'account id invalid'})
            recipes = []
            for recipe_id in cursor.get('favorites'):
                recipe_cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
                if recipe_cursor == None:
                    continue
                recipes.append(recipe_cursor)

            bson_to_json = dumps(recipes)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'recipes':true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

class User_Recipes(Resource):
    @jwt_required()
    def get(self):
        try:
            db = client.exechef
            _account_id = dict(current_identity).get('user_id')
            #return list of recipes from user {'userFavorites': []}
            cursor = db.accounts.find_one({'_id': ObjectId(_account_id)})
            if cursor == None:
                return jsonify({'error': 'account id invalid'})
            recipes = []
            for recipe_id in cursor.get('created'):
                recipe_cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
                if recipe_cursor == None:
                    continue
                recipes.append(recipe_cursor)

            bson_to_json = dumps(recipes)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'recipes':true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})


class Recipes(Resource):
    def get(self):
        try:
            db = client.exechef
            cursor = db.recipes.find()
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'recipes': true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

class Recipe(Resource):
    def get(self, recipe_id):
        try:
            db = client.exechef
            cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
            if cursor == None:
                return jsonify({'error': 'recipe not found'})
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'recipe': true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

class Update_Recipe(Resource):
    @jwt_required()
    def put(self):
        try:
            #these are the fields we want to be able to update
            acceptable_entries = [
                'name',
                'tags',
                'steps',
                'description',
                'private',
                'ingredients',
            ]
            db = client.exechef

            json_data = request.get_json(force=True)

            recipe_id = json_data['id']

            #verifies user attempting to modify recipe owns the recipe
            _account_id = dict(current_identity).get('user_id')
            users_account = db.accounts.find_one({'_id': ObjectId(_account_id)})
            if recipe_id not in users_account['created']:
                return jsonify({'error':'User does not have permission to modify this recipe'})

            to_update = {}
            #removes stuff we don't want to update and updates modified date
            for key, value in json_data.iteritems():
                if key in acceptable_entries:
                    to_update[key] = value
            to_update['modified_date'] = datetime.now()

            result = db.recipes.update_one(
                {'_id': ObjectId(recipe_id)},
                {
                    '$set': to_update
                }
            )
            if result.modified_count == 1:
                return jsonify({'updated' : True})
            else:
                return jsonify({'updated': False})
        except Exception as e:
            return jsonify({'error':str(e)})

class Create_Recipe(Resource):
    @jwt_required()
    def post(self):
        try:
            db = client.exechef
            json_data = request.get_json(force=True)
            name = json_data['name']
            tags = json_data['tags']
            steps = json_data['steps']
            description = json_data['description']
            private = json_data['private']
            ingredients = json_data['ingredients']#[]

            #get author directly from the user logged in to prevent someone
            #from trying to make it appear another person made the recipe
            _account_id = dict(current_identity).get('user_id')
            users_account = db.accounts.find_one({'_id': ObjectId(_account_id)})
            username = users_account['username']

            result = db.recipes.insert_one(
            {
                'name' : name,
                'tags' : tags,
                'steps' : steps,
                'author' : username,
                'description' : description,
                'private' : private,
                'ingredients' : ingredients,
                'created_date' : datetime.now(),
                'modified_date' : datetime.now()
            })

            #add recipe to user's created recipes
            db.accounts.update({'username': username}, {'$push': {'created': str(result.inserted_id)}})
            #return the id of the new recipe
            return jsonify({'id': str(result.inserted_id)})

            #add password getting, encrypting, and comparison
        except Exception as e:
            return jsonify({'error': str(e)})
        pass

class Delete_Recipe(Resource):
    @jwt_required()
    def delete(self, recipe_id):
        try:
            db = client.exechef

            #change recipe_id to BSON id format
            recipe_id = ObjectId(recipe_id)

            #verifies user attempting to delete recipe owns the recipe
            _account_id = dict(current_identity).get('user_id')
            users_account = db.accounts.find_one({'_id': ObjectId(_account_id)})
            if recipe_id not in users_account['created']:
                return jsonify({'error':'User does not have permission to delete this recipe'})

            result = db.recipes.delete_one({'_id': recipe_id})
            if result.deleted_count == 1:
                return jsonify({'deleted': True})
            else:
                return jsonify({'deleted': False})
        except Exception as e:
            return jsonify({'error':str(e)})

#search all recipe fields by a string, return recipes with found string
#need to make it non case sensitive
class Search_Tags(Resource):
    def get(self, tag_str):
        try:
            db = client.exechef
            cursor = db.recipes.find({'tags': re.compile(tag_str, re.IGNORECASE), 'private': 'False'})
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            return jsonify({'recipes': true_json_data})
        except Exception as e:
            return jsonify({'error':str(e)})

jwt = JWT(app, authenticate, identity)
api.add_resource(Accounts, '/Accounts')
api.add_resource(Account, '/Account')
api.add_resource(Update_Password, '/UpdatePassword')
api.add_resource(Create_Account, '/CreateAccount')
api.add_resource(Favorites, '/Favorites')
api.add_resource(User_Recipes, '/UserRecipes')
api.add_resource(Recipes, '/Recipes')
api.add_resource(Recipe, '/Recipes/<recipe_id>')
api.add_resource(Update_Recipe, '/UpdateRecipe')
api.add_resource(Create_Recipe, '/CreateRecipe')
api.add_resource(Delete_Recipe, '/DeleteRecipe/<recipe_id>')
api.add_resource(Search_Tags, '/SearchTags/<tag_str>')


@app.route('/')
def render_startpage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port='5000')
