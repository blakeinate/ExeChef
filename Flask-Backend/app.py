from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse, abort
from flask import jsonify, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt, jwt_optional
)
from flask_pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from validate_email import validate_email
from datetime import datetime
import json
import re
import os.path
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'the most secret key ever'
app.config['JWT_SECRET_KEY'] = 'the most secret key ever'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)
client = MongoClient()
db = client['exechef']

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    try:
        jti = decrypted_token['jti']
        cursor = db.blacklist.find_one({'token': str(jti)})
        if cursor:
            return True
        else:
            return False
    except Exception as e:
        return False

#upon logout store keys in blacklist
def add_to_blacklist(jti):
    try:
        result = db.blacklist.insert_one(
        {
            'token': str(jti)
        })
        return True
    except Exception as e:
        return False

def allowed_file(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return True
    return False


#uploads image to server and returns secure filename
def upload_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #make sure filename is unique in folder
        if os.path.isfile(app.config['UPLOAD_FOLDER'] + filename):
            good_filename = False
            count = 0
            #if not unique, append count to beginning of filename until it is unique
            while(not good_filename):
                if os.path.isfile(app.config['UPLOAD_FOLDER'] + str(count) + filename) == False:
                    filename = str(count) + filename
                    good_filename = True
                else:
                    count = count + 1
        #save to upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return None


class Users(Resource):
    def get(self):
        cursor = db.accounts.find()
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'users': true_json_data})
        resp.status_code = 200
        return resp


class User(Resource):
    @jwt_optional
    def get(self, username=None):
        _account_name = get_jwt_identity()
        current_user = None
        if _account_name:
            current_user = db.accounts.find_one({'username': _account_name})
        if username:
            provided_user = db.accounts.find_one({'username': str(username)}, {'password': 0, 'email': 0})
            if not provided_user:
                abort(400, message='No account found associated with provided id.')
            bson_to_json = dumps(provided_user)
            true_json_data = json.loads(bson_to_json)
            if current_user:
                if provided_user.get('username') in current_user.get('followed'):
                    followed = True
                else:
                    followed = False
                true_json_data['followed'] = followed
            resp = jsonify({'user': true_json_data})
            resp.status_code = 200
        else:
            if current_user == None:
                abort(400, message='No account found associated with provided access token.')
            bson_to_json = dumps(current_user)
            true_json_data = json.loads(bson_to_json)
            resp = jsonify({'user': true_json_data})
            resp.status_code = 200

        return resp

    @jwt_required
    def put(self):
        acceptable_entries = ['bio']#, 'old_password', 'new_password', 'favorites']
        json_data = request.get_json(force=True)
        _old_password = json_data.get('old_password')
        _new_password = json_data.get('new_password')
        _account_email = json_data.get('email')
        favorites = json_data.get('favorites')
        followed = json_data.get('followed')
        followers = json_data.get('followers')
        _account_name = get_jwt_identity()

        if not _account_name:
            abort(422, message='The provided username is invalid.')

        to_update = {}

        if _account_email:
            if validate_email(str(_account_email)):
                cursor2 = db.accounts.find_one({'email': str(_account_email)})
                if cursor2 != None:
                    abort(422, message='The email provided is already in use.')
                else:
                    to_update['email'] = str(_account_email)
            else:
                abort(422, message='The provided email is invalid.')

        #removes stuff we don't want to update and updates modified date
        for key, value in json_data.iteritems():
            if key in acceptable_entries:
                to_update[key] = value

        #make sure both passwords provided or none at all, otherwise send back we need both of them
        passwords_provided = False
        if _old_password:
            if _new_password:
                passwords_provided = True
            else:
                abort(422, message='The provided new password is invalid.')
        if _new_password:
            if _old_password:
                passwords_provided = True
            else:
                abort(422, message='The provided old password is invalid.')

        #make sure old pass provided matches stored password
        if passwords_provided:
            cursor = db.accounts.find_one({'username': _account_name})
            if cursor['password'] == _old_password:
                to_update['password'] = _new_password
            else:
                abort(422, 'The current password does not match the password provided.')

        if favorites:
            to_update['favorites'] = favorites

        if followed:

            #remove user from the followers lists of users no longer followed
            user_info = db.accounts.find_one({'username': _account_name})
            removed_users = []
            for followed_user in user_info.get('followed'):
                if followed_user not in followed:
                    removed_users.append({'username': followed_user})
            if removed_users:
                result = db.accounts.update({'$or': removed_users}, {'$pull': {'followers': str(_account_name)}})
                if result.modified_count == 0:
                    abort(500, message = "Unable to remove user from the follower lists of the user(s) removed from users following list.")

            #add user to the followers list of users now followed
            added_users = []
            for followed_user in followed:
                if followed_user not in user_info.get('followed'):
                    added_users.append({'username': followed_user})
            if added_users:
                result = db.accounts.update({'$or': removed_users}, {'$push': {'followers': str(_account_name)}})
                if result.modified_count == 0:
                    abort(500, message="Unable to add user to the follower lists of the user(s) added to users following list.")

            to_update['followed'] = followed

        if followers:
            to_update['followers'] = followers

        #return list of recipes from user {'userFavorites': []}
        cursor = db.accounts.find_one({'username': str(_account_name)})

        to_change = {}
        if to_update:
            to_change['$set'] = to_update

        if to_change:
            result = db.accounts.update_one(
                {'username': str(_account_name)},
                to_change
            )

            if result.modified_count == 1:
                cursor = db.accounts.find_one({'username': str(_account_name)})
                bson_to_json = dumps(cursor)
                true_json_data = json.loads(bson_to_json)
                resp = jsonify({'user': true_json_data})
                resp.status_code = 200
                return resp
            else:
                abort(500, message='Unable to communicate with database and/or account modification failed.')
        else:
            abort(422, message='No data provided to update')


    def post(self):
        json_data = request.get_json(force=True)

        _account_name = json_data.get('username')
        _account_password = json_data.get('password')
        _account_email = json_data.get('email')

        if not _account_name:
            abort(422, message='The provided username is invalid.')
        if not _account_password:
            abort(422, message='The provided password is invalid.')
        if not validate_email(str(_account_email)):
            abort(422, message='The provided email is invalid.')
        #add password stuff here, encrypting and uploading

        #check if username exists
        cursor = db.accounts.find_one({'username': str(_account_name)})
        if cursor != None:
            abort(422, message='The username provided is already in use.')

        cursor2 = db.accounts.find_one({'email': str(_account_email)})
        if cursor2 != None:
            abort(422, message='The email provided is already in use.')

        #upload new account info to pymongo db
        result = db.accounts.insert_one(
        {
            'username': _account_name,
            'password': _account_password,
            'email': _account_email,
            'favorites': [],
            'followers': [],
            'created': [],
            'bio': '',
        })
        created = db.accounts.find_one({'username': _account_name})
        bson_to_json = dumps(created)
        true_json_data = json.loads(bson_to_json)
        #return the id of the new account
        resp = jsonify({'user': true_json_data})
        resp.status_code = 200
        return resp


class Update_Password(Resource):
    @jwt_required
    def put(self):
        json_data = request.get_json(force=True)

        _account_name = get_jwt_identity()
        _old_password = json_data.get('old_password')
        _new_password = json_data.get('new_password')
        if not _account_name:
            abort(422, message='The provided username is invalid.')
        if not _old_password:
            abort(422, message='The provided old password is invalid.')
        if not _new_password:
            abort(422, message='The provided new password is invalid.')

        cursor = db.accounts.find_one({'username': _account_name})
        if cursor['password'] == _old_password:
            result = db.accounts.update_one(
                {'username': _account_name},
                {
                    '$set': {
                        'password': _new_password
                    }
                }
            )
            if result.modified_count == 1:
                return Response(status=200)
            else:
                abort(500, message='Password could not be updated. Database could not modify the specified account.')
        else:
            abort(422,'The current password does not match the password provided.')


#checks if a username and password match
class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        _account_login = json_data.get('login')
        _account_password = json_data.get('password')


        #need to add password encrypting, and comparison

        if _account_login:
            if validate_email(str(_account_login)):
                cursor = db.accounts.find_one({'email': str(_account_login)})
            else:
                cursor = db.accounts.find_one({'username': str(_account_login)})
        else:
            abort(422, message='Please provide a valid username/email.')


        if cursor == None:
            abort(422, message='The username/email provided is not associated with an active account.')
        if cursor.get('password') == _account_password:
            _access_token = create_access_token(identity=cursor.get('username'))
            _refresh_token = create_refresh_token(identity=cursor.get('username'))
            bson_to_json = dumps(cursor)
            true_json_data = json.loads(bson_to_json)
            true_json_data['access_token'] = _access_token
            true_json_data['refresh_token'] = _refresh_token
            resp = jsonify({
                'user': true_json_data
            })
            resp.status_code = 200
            return resp
        else:
            abort(422, message='The current password does not match the password provided.')



#creates a new access token
class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            _access_token = create_access_token(identity=current_user)
            resp = jsonify({'access_token': _access_token})
            resp.status_code = 200
            return resp
        except Exception as e:
            abort(500, message=str(e))


#blacklists jwt access token
class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        result = add_to_blacklist(jti)
        if result:
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database.')


#blacklists jwt refresh token
class Logout2(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        result = add_to_blacklist(jti)
        if result:
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database.')


#returns list of recipes from user's favorites list
class Favorites(Resource):
    @jwt_required
    def get(self):
        _account_name = get_jwt_identity()
        #return list of recipes from user {'userFavorites': []}
        cursor = db.accounts.find_one({'username': str(_account_name)})
        if cursor == None:
            abort(400, message='No user found associated with provided access token.')
        recipes = []
        for recipe_id in cursor.get('favorites'):
            recipe_cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
            if recipe_cursor == None:
                continue
            recipes.append(recipe_cursor)

        bson_to_json = dumps(recipes)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes':true_json_data})
        resp.status_code = 200
        return resp


#returns list of recipes created by the current user from their created list
class User_Recipes(Resource):
    @jwt_required
    def get(self):
        _account_name = get_jwt_identity()
        #return list of recipes from user {'userFavorites': []}
        cursor = db.accounts.find_one({'username': str(_account_name)})
        if cursor == None:
            abort(400, message='No user found associated with provided access token.')
        recipes = []
        for recipe_id in cursor.get('created'):
            recipe_cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
            if recipe_cursor == None:
                continue
            recipes.append(recipe_cursor)

        bson_to_json = dumps(recipes)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes':true_json_data})
        resp.status_code = 200
        return resp

#get feed composed of followed accounts recent recipes
class Followed_Feed(Resource):
    @jwt_optional
    def get(self, num_to_get = 10):
        num_to_get = int(num_to_get)
        _account_name = get_jwt_identity()
        if _account_name:
            followed = db.accounts.find_one({'username': str(_account_name)}).get('followed')
            followed_list = []
            for item in followed:
                followed_list.append({'author': item})
            recent_recipes = db.recipes.find({'$or': followed_list, 'private':'False'}).limit(num_to_get).sort('created_date.$date', -1)
        else:
            recent_recipes = db.recipes.find({'private': 'False'}).limit(num_to_get).sort('created_date.$date', -1)
        bson_to_json = dumps(recent_recipes)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes': true_json_data})
        resp.status_code = 200
        return resp

#returns list of all recipes
class Recipes(Resource):
    def get(self):
        cursor = db.recipes.find()
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes': true_json_data})
        resp.status_code = 200
        return resp


#returns a single recipe
class Recipe(Resource):
    @jwt_required
    def post(self):
        #check if image provided
        image = None;
        if 'file' in request.files:
            image = request.files['file']
            if image.filename == '':
                image = None

        json_data = request.get_json(force=True)
        name = json_data.get('name')
        tags = json_data.get('tags')
        steps = json_data.get('steps')
        description = json_data.get('description')
        private = json_data.get('private')
        ingredients = json_data.get('ingredients')

        if (not name) or (not private) or (not ingredients) or (not steps):
            abort(422, message='Some required fields were not provided.')

        #upload image and get secure filename
        secure_filename = None
        if image:
            secure_filename = upload_image(image)

        #get author directly from the user logged in to prevent someone
        #from trying to make it appear another person made the recipe
        _account_name = get_jwt_identity()

        result = db.recipes.insert_one(
        {
            'name' : name,
            'image_name': secure_filename,
            'tags' : tags,
            'steps': steps,
            'author': _account_name,
            'description' : description,
            'private' : private,
            'ingredients' : ingredients,
            'created_date' : datetime.now(),
            'modified_date' : datetime.now()
        })

        #add recipe to user's created recipes
        db.accounts.update({'username': _account_name}, {'$push': {'created': str(result.inserted_id)}})
        #return the id of the new recipe
        resp = jsonify({'id': str(result.inserted_id)})
        resp.status_code = 201
        return resp

        #add password getting, encrypting, and comparison

    @jwt_optional
    def get(self, recipe_id):
        cursor = db.recipes.find_one({'_id': ObjectId(recipe_id)})
        if cursor == None:
            abort(400, message='No recipe found with the provided recipe ID.')
        if (cursor.get('author') != get_jwt_identity()) and (cursor.get('private') == 'True'):
            abort(403, message='Private recipe is owned by another user.')
        author = db.accounts.find_one({'username': str(cursor.get('author'))}, {'password': 0, 'email': 0})
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
        true_json_data['user'] = author
        resp = jsonify({'recipe': true_json_data})
        resp.status_code = 200
        return resp

    @jwt_required
    def put(self):
        # these are the fields we want to be able to update
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

        # verifies user attempting to modify recipe owns the recipe
        _account_name = get_jwt_identity()
        users_account = db.accounts.find_one({'username': str(_account_name)})
        if recipe_id not in users_account.get('created'):
            abort(403, message='Recipe is owned by another user. Modifications are not allowed.')

        to_update = {}
        # removes stuff we don't want to update and updates modified date
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
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database and/or recipe modification failed.')

    @jwt_required
    def delete(self, recipe_id):

        # change recipe_id to BSON id format
        recipe_id = ObjectId(recipe_id)

        # verifies user attempting to delete recipe owns the recipe
        _account_name = get_jwt_identity()
        users_account = db.accounts.find_one({'username': _account_name})
        if recipe_id not in users_account['created']:
            abort(403, message='Recipe is owned by another user. Modifications are not allowed.')

        result = db.recipes.delete_one({'_id': recipe_id})
        if result.deleted_count == 1:
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database and/or recipe modification failed.')








#search all recipe fields by a string, return recipes with found string
#MAKE SURE THIS WORKS
class Search_Tags(Resource):
    def get(self, tag_str):
        #split string and remove non alphanumeric
        tag_list = [{'tags': re.compile(''.join(c for c in string if c.isalnum()), re.IGNORECASE)} for string in tag_str.split(',')]
        cursor = db.recipes.find({'$or': tag_list, 'private': 'False'})
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes': true_json_data})
        resp.status_code = 200
        return resp

class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count



api.add_resource(Login, '/Login')
api.add_resource(Followed_Feed, '/Feed/<num_to_get>', '/Feed')
api.add_resource(Logout, '/Logout')
api.add_resource(Logout2, '/Logout2')
api.add_resource(Refresh, '/Refresh')
api.add_resource(Users, '/Users')
api.add_resource(User, '/User/<username>', '/User')
api.add_resource(Update_Password, '/UpdatePassword')
#api.add_resource(Create_Account, '/CreateAccount')
api.add_resource(Favorites, '/Favorites')
api.add_resource(User_Recipes, '/UserRecipes')
api.add_resource(Recipes, '/Recipes')
api.add_resource(Recipe, '/Recipe/<recipe_id>', '/Recipe')
#api.add_resource(Create_Recipe, '/CreateRecipe')
#api.add_resource(Delete_Recipe, '/DeleteRecipe/<recipe_id>')
api.add_resource(Search_Tags, '/SearchTags/<tag_str>')


@app.route('/')
def render_startpage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5000)
