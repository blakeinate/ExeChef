from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask import jsonify
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from datetime import datetime
import json
app = Flask(__name__)
api = Api(app)

client = MongoClient()

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
    def get(self, _account_id):
        try:
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
            return jsonify({'id': str(result.inserted_id)})
        except Exception as e:
            return jsonify({'error': str(e)})

class Favorites(Resource):
    def get(self, account_id):
        try:
            db = client.exechef
            #return list of recipes from user {'userFavorites': []}
            pass
        except Exception as e:
            return jsonify({'error':str(e)})

class User_Recipes(Resource):
    def get(self, account_id):
        try:
            db = client.exechef
            #return list of recipes from user {'userRecipes': []}
            pass
        except Exception as e:
            return jsonify({'error':str(e)})

class Authenticate_User(Resource):
    def post(self):
        try:
            db = client.exechef
            json_data = request.get_json(force=True)
            _account_name = json_data['username']
            _account_password = json_data['password']

            #add password getting, encrypting, and comparison

            cursor = db.accounts.find_one({'username': _account_name})
            if cursor == None:
                return jsonify({'error': 'account not found'})
            if cursor['password'] == _account_password:
                return jsonify({'id': str(cursor['_id'])})
            else:
                return jsonify({'error': 'incorrect password'})

        except Exception as e:
            return jsonify({'error': str(e)})

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
    def put(self):
        try:
            db = client.exechef
            #returns {'updated': True} or False
            pass
        except Exception as e:
            return jsonify({'error':str(e)})

class Create_Recipe(Resource):
    def post(self):
        try:
            db = client.exechef
            json_data = request.get_json(force=True)
            name = json_data['name']
            category = json_data['category']
            steps = json_data['steps']
            author = json_data['author']
            description = json_data['description']
            private = json_data['private']
            ingredients = json_data['ingredients']#[]

            result = db.recipes.insert_one(
            {
                'name' : name,
                'category' : category,
                'steps' : steps,
                'author' : author,
                'description' : description,
                'private' : private,
                'ingredients' : ingredients,
                'created_date' : datetime.now(),
                'modified_date' : datetime.now()
            })
            #return the id of the new recipe
            return jsonify({'id': str(result.inserted_id)})

            #add password getting, encrypting, and comparison
        except Exception as e:
            return jsonify({'error': str(e)})
        pass

class Delete_Recipe(Resource):
    def delete(self):
        try:
            db = client.exechef
            #return {'deleted': True} if deleted, otherwise false
            pass
        except Exception as e:
            return jsonify({'error':str(e)})

#search all recipe fields by a string, return recipes with found string
class Search_Recipes(Resource):
    def get(self, recipe_str):
        try:
            db = client.exechef
            #return list of recipes matching criteria {'recipes' : []}
            pass
        except Exception as e:
            return jsonify({'error':str(e)})


api.add_resource(Accounts, '/Accounts')
api.add_resource(Account, '/Accounts/<_account_id>')
api.add_resource(Update_Password, '/UpdatePassword')
api.add_resource(Create_Account, '/CreateAccount')
api.add_resource(Favorites, '/Favorites/<account_id>')
api.add_resource(User_Recipes, '/UserRecipes/<account_id>')
api.add_resource(Authenticate_User, '/Authenticate')
api.add_resource(Recipes, '/Recipes')
api.add_resource(Recipe, '/Recipes/<recipe_id>')
api.add_resource(Update_Recipe, '/UpdateRecipe')
api.add_resource(Create_Recipe, '/CreateRecipe')
api.add_resource(Delete_Recipe, '/DeleteRecipe')
api.add_resource(Search_Recipes, '/SearchRecipe/<recipe_str>')


if __name__ == '__main__':
    app.run(port='5000')
