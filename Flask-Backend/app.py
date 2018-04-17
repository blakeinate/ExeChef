from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse, abort
from flask import jsonify, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt, jwt_optional
)
from flask_pymongo import PyMongo
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
client = PyMongo(app)
#db = client['exechef']

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
        cursor = client.db.blacklist.find_one({'token': str(jti)})
        if cursor:
            return True
        else:
            return False
    except Exception as e:
        return False

#upon logout store keys in blacklist
def add_to_blacklist(jti):
    try:
        result = client.db.blacklist.insert_one(
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
def upload_image(file, username):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'] + str(username))
        except OSError:
            pass
        #make sure filename is unique in folder
        if os.path.isfile(app.config['UPLOAD_FOLDER'] + str(username) + '/' + filename):
            good_filename = False
            count = 0
            #if not unique, append count to beginning of filename until it is unique
            while(not good_filename):
                if os.path.isfile(app.config['UPLOAD_FOLDER'] + str(username) + '/' + str(count) + filename) == False:
                    filename = str(count) + filename
                    good_filename = True
                else:
                    count = count + 1

        #save to upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(username) + '/', filename))
        return filename
    else:
        return None


def remove_old_image(filename, username):
    if os.path.isfile(app.config['UPLOAD_FOLDER'] + str(username) + '/' +filename):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER']+ str(username) + '/', filename))
        return True
    else:
        return False


def handle_recipe_image(recipe_request, username, recipe_id=None):
    # upload image for recipe
    image = None;
    if 'file' in recipe_request.files:
        image = recipe_request.files['image']
        if image.filename == '':
            image = None
    # upload image and get secure filename
    image_filename = None
    if image:
        image_filename = upload_image(image, username)
    if image_filename:
        if recipe_id:
            recipe = client.db.recipes.find_one({'_id': ObjectId(recipe_id)})
            if recipe.get('image_name'):
                remove_old_image(recipe.get('image_name'), username)
        return image_filename
    else:
        return None


def handle_user_image(user_request, username):
    # upload image for recipe
    image = None;
    if 'file' in user_request.files:
        image = user_request.files['image']
        if image.filename == '':
            image = None
    # upload image and get secure filename
    image_filename = None
    if image:
        image_filename = upload_image(image, username)
    if image_filename:
        if username:
            user = client.db.accounts.find_one({'username': username})
            if user.get('image_name'):
                remove_old_image(user.get('image_name'), username)
        return image_filename
    else:
        return None

class Users(Resource):
    def get(self):
        cursor = client.db.accounts.find()
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
            current_user = client.db.accounts.find_one({'username': _account_name})
        if username:
            provided_user = client.db.accounts.find_one({'username': str(username)}, {'password': 0, 'email': 0})
            if not provided_user:
                abort(400, message='No account found associated with provided id.')
            bson_to_json = dumps(provided_user)
            true_json_data = json.loads(bson_to_json)
            if current_user:
                if isinstance(current_user.get('following'), (list,)):
                    if provided_user.get('username') in current_user.get('following'):
                        am_i_following = True
                    else:
                        am_i_following = False
                else:
                    am_i_following = False
                true_json_data['am_i_following'] = am_i_following
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
        acceptable_entries = ['bio']
        json_data = request.get_json(force=True)
        _old_password = json_data.get('old_password')
        _new_password = json_data.get('new_password')
        _account_email = json_data.get('email')
        favorites = json_data.get('favorites')
        following = json_data.get('following')
        followers = json_data.get('followers')
        user_image = json_data.get('image_name')
        _account_name = get_jwt_identity()

        if not _account_name:
            abort(422, message='The provided username is invalid.')

        to_update = {}

        #if new email provided make sure its valid
        if _account_email:
            if validate_email(str(_account_email)):
                cursor2 = client.db.accounts.find_one({'email': str(_account_email)})
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
            cursor = client.db.accounts.find_one({'username': _account_name})
            if cursor['password'] == _old_password:
                to_update['password'] = _new_password
            else:
                abort(422, message='The current password does not match the password provided.')

        self.update_favorites(favorites, _account_name)

        to_update['favorites'] = favorites

        self.update_following(following, _account_name)

        to_update['following'] = following

        if isinstance(followers, (list,)):
            to_update['followers'] = followers

        #return list of recipes from user {'userFavorites': []}
        cursor = client.db.accounts.find_one({'username': str(_account_name)})

        image_filename = handle_user_image(request, _account_name)
        if image_filename:
            to_update['image_name'] = image_filename

        if user_image == 'remove':
            user = client.db.accounts.find_one({'username': _account_name})
            if user.get('image_name'):
                remove_old_image(user.get('image_name'), _account_name)
            to_update['image_name'] = None

        to_change = {}
        if to_update:
            to_change['$set'] = to_update

        if to_change:
            result = client.db.accounts.update_one(
                {'username': str(_account_name)},
                to_change
            )
            if result.acknowledged:
                cursor = client.db.accounts.find_one({'username': str(_account_name)})
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
        cursor = client.db.accounts.find_one({'username': str(_account_name)})
        if cursor != None:
            abort(422, message='The username provided is already in use.')

        cursor2 = client.db.accounts.find_one({'email': str(_account_email)})
        if cursor2 != None:
            abort(422, message='The email provided is already in use.')

        #upload new account info to pymongo client.db
        result = client.db.accounts.insert_one(
        {
            'username': _account_name,
            'password': _account_password,
            'email': _account_email,
            'favorites': [],
            'followers': [],
            'following': [],
            'created': [],
            'bio': '',
            'image_name': None
        })
        created = client.db.accounts.find_one({'username': _account_name})
        bson_to_json = dumps(created)
        true_json_data = json.loads(bson_to_json)
        #return the id of the new account
        resp = jsonify({'user': true_json_data})
        resp.status_code = 200
        return resp

    def update_following(self, following, _account_name):
        if isinstance(following, (list,)):
            #remove user from the followers lists of users no longer following
            user_info = client.db.accounts.find_one({'username': _account_name})
            removed_users = []
            if user_info.get('following'):
                for following_user in user_info.get('following'):
                    if following_user not in following:
                        removed_users.append({'username': following_user})
            if removed_users:
                result = client.db.accounts.update_many({'$or': removed_users}, {'$pull': {'followers': str(_account_name)}})
                if not result.acknowledged:
                    abort(500, message = "Unable to remove user from the follower lists of the user(s) removed from users following list.")

            #add user to the followers list of users now following
            added_users = []
            if isinstance(user_info.get('following'), (list,)):
                for following_user in following:
                    if following_user not in user_info.get('following'):
                        added_users.append({'username': following_user})
            else:
                for following_user in following:
                    added_users.append({'username': following_user})

            if added_users:
                result = client.db.accounts.update_many({'$or': added_users}, {'$push': {'followers': str(_account_name)}})
                if not result.acknowledged:
                    abort(500, message="Unable to add user to the follower lists of the user(s) added to users following list.")
        return

    def update_favorites(self, favorites, _account_name):
        #increment or decrement favorited_count for new or removed recipes from favorites
        if isinstance(favorites, (list,)):
            user_info = client.db.accounts.find_one({'username': _account_name})
            removed_favorites = []
            if user_info.get('favorites'):
                for favorited_recipe in user_info.get('favorites'):
                    if favorited_recipe not in favorites:
                        removed_favorites.append({'_id': ObjectId(favorited_recipe)})
            if removed_favorites:
                result = client.db.recipes.update_many({'$or': removed_favorites},
                                                        {'$inc': {'favorited_count': -1}})
                if not result.acknowledged:
                    abort(500,
                          message="Unable to remove user from the follower lists of the user(s) removed from users following list.")
            added_favorites = []
            if isinstance(user_info.get('favorites'), (list,)):
                for favorited_recipe in favorites:
                    if favorited_recipe not in user_info.get('favorites'):
                        added_favorites.append({'_id': favorited_recipe})
            else:
                for favorited_recipe in favorites:
                    added_favorites.append({'_id': favorited_recipe})

            if added_favorites:
                result = client.db.recipes.update_many({'$or': added_favorites}, {'$inc': {'favorited_count': 1}})
                if not result.acknowledged:
                    abort(500, message="Unable to add user to the follower lists of the user(s) added to users following list.")
        return

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

        cursor = client.db.accounts.find_one({'username': _account_name})
        if cursor['password'] == _old_password:
            result = client.db.accounts.update_one(
                {'username': _account_name},
                {
                    '$set': {
                        'password': _new_password
                    }
                }
            )
            if result.acknowledged:
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
                cursor = client.db.accounts.find_one({'email': str(_account_login)})
            else:
                cursor = client.db.accounts.find_one({'username': str(_account_login)})
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
        cursor = client.db.accounts.find_one({'username': str(_account_name)})
        if cursor == None:
            abort(400, message='No user found associated with provided access token.')
        recipes = []
        if isinstance(cursor.get('favorites'), (list,)):
            for recipe_id in cursor.get('favorites'):
                recipe_cursor = client.db.recipes.find_one({'_id': ObjectId(recipe_id)})
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
        cursor = client.db.accounts.find_one({'username': str(_account_name)})
        if cursor == None:
            abort(400, message='No user found associated with provided access token.')
        recipes = []
        if isinstance(cursor.get('created'), (list,)):
            for recipe_id in cursor.get('created'):
                recipe_cursor = client.db.recipes.find_one({'_id': ObjectId(recipe_id)})
                if recipe_cursor == None:
                    continue
                recipes.append(recipe_cursor)

        bson_to_json = dumps(recipes)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes':true_json_data})
        resp.status_code = 200
        return resp

#get feed composed of following accounts recent recipes
class Following_Feed(Resource):
    @jwt_optional
    def get(self, num_to_get = 10):
        num_to_get = int(num_to_get)
        _account_name = get_jwt_identity()
        if _account_name:
            following = client.db.accounts.find_one({'username': str(_account_name)}).get('following')
            following_list = []
            if isinstance(following, (list,)):
                for item in following:
                    following_list.append({'author': item})
                recent_recipes = client.db.recipes.find({'$or': following_list, 'private':'False'}).limit(num_to_get).sort('created_date.$date', -1)
        else:
            recent_recipes = client.db.recipes.find({'private': 'False'}).limit(num_to_get).sort('created_date.$date', -1)
        bson_to_json = dumps(recent_recipes)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes': true_json_data})
        resp.status_code = 200
        return resp

#returns list of all recipes
class Recipes(Resource):
    def get(self):
        cursor = client.db.recipes.find()
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
        resp = jsonify({'recipes': true_json_data})
        resp.status_code = 200
        return resp


class Recipe(Resource):
    @jwt_required
    def post(self):

        json_data = request.get_json(force=True)
        name = json_data.get('recipe').get('name')
        tags = json_data.get('recipe').get('tags')
        steps = json_data.get('recipe').get('steps')
        description = json_data.get('recipe').get('description')
        private = json_data.get('recipe').get('private')
        ingredients = json_data.get('recipe').get('ingredients')
        recipe_image = json_data.get('recipe').get('image_name')

        if (name == None) or (private == None) or (ingredients == None) or (steps == None):
            abort(422, message='Some required fields were not provided.')

        #get author directly from the user logged in to prevent someone
        #from trying to make it appear another person made the recipe
        _account_name = get_jwt_identity()

        image_filename = None
        image_name = handle_recipe_image(request, _account_name)
        if image_name:
            image_filename = image_name


        result = client.db.recipes.insert_one(
        {
            'name' : name,
            'image_name': image_filename,
            'tags': tags,
            'steps': steps,
            'author': _account_name,
            'description': description,
            'private': private,
            'ingredients': ingredients,
            'created_date': datetime.now(),
            'modified_date': datetime.now(),
            'favorited_count': 0
        })

        #add recipe to user's created recipes
        client.db.accounts.update({'username': _account_name}, {'$push': {'created': str(result.inserted_id)}})

        #return the new recipe
        recipe = client.db.recipes.find_one({'_id': result.inserted_id})
        bson_to_json = dumps(recipe)
        true_json_data = json.loads(bson_to_json)
        print true_json_data
        resp = jsonify({'recipe': true_json_data})
        resp.status_code = 201
        return resp

        #add password getting, encrypting, and comparison

    @jwt_optional
    def get(self, recipe_id):
        cursor = client.db.recipes.find_one({'_id': ObjectId(recipe_id)})
        if cursor == None:
            abort(400, message='No recipe found with the provided recipe ID.')
        if (cursor.get('author') != get_jwt_identity()) and (cursor.get('private') == 'True'):
            abort(403, message='Private recipe is owned by another user.')

        favorited = False

        if get_jwt_identity():
            current_user = client.db.accounts.find_one({'username': str(get_jwt_identity())}, {'password': 0, 'email': 0})
            if isinstance(current_user.get('favorites'), (list,)):
                if str(recipe_id) in current_user.get('favorites'):
                    favorited = True

        author = client.db.accounts.find_one({'username': str(cursor.get('author'))}, {'password': 0, 'email': 0})
        cursor['user'] = author
        cursor['in_favorites'] = favorited
        bson_to_json = dumps(cursor)
        true_json_data = json.loads(bson_to_json)
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

        json_data = request.get_json(force=True)
        recipe_image = json_data.get('recipe').get('image_name')
        recipe_id = json_data.get('recipe').get('id')
        if not recipe_id:
            abort(422, message='No recipe ID provided.')

        # verifies user attempting to modify recipe owns the recipe
        _account_name = get_jwt_identity()
        users_account = client.db.accounts.find_one({'username': str(_account_name)})
        if isinstance(users_account.get('created'), (list,)):
            if recipe_id not in users_account.get('created'):
                abort(403, message='Recipe is owned by another user. Modifications are not allowed.')
        else:
            abort(403, message='Recipe is owned by another user. Modifications are not allowed.')
        to_update = {}

        image_name = handle_recipe_image(request, _account_name, recipe_id)
        if image_name:
            to_update['image_name'] = image_name

        if recipe_image == 'remove':
            recipe = client.db.recipes.find_one({'_id': ObjectId(recipe_id)})
            if recipe.get('image_name'):
                remove_old_image(recipe.get('image_name'), _account_name)
            to_update['image_name'] = None


        # removes stuff we don't want to update and updates modified date
        for key, value in json_data.get('recipe').iteritems():
            if key in acceptable_entries:
                to_update[key] = value


        if not to_update:
            abort(422, message='No data provided to update')

        to_update['modified_date'] = datetime.now()

        result = client.db.recipes.update_one(
            {'_id': ObjectId(recipe_id)},
            {
                '$set': to_update
            }
        )
        if result.acknowledged:
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database and/or recipe modification failed.')

    @jwt_required
    def delete(self, recipe_id):
        # change recipe_id to BSON id format
        recipe_id = ObjectId(recipe_id)

        # verifies user attempting to delete recipe owns the recipe
        _account_name = get_jwt_identity()
        users_account = client.db.accounts.find_one({'username': _account_name})
        if str(recipe_id) not in users_account['created']:
            abort(403, message='Recipe is owned by another user. Modifications are not allowed.')

        favorited_by = client.db.accounts.find({'favorites': [str(recipe_id)]})

        users_to_remove = []
        for user in favorited_by:
            users_to_remove.append({'username': user.get('username')})

        #delete image since recipe will be deleted
        recipe = client.db.recipes.find_one({'_id': recipe_id})
        image_filename = recipe.get('image_name')
        if image_filename:
            remove_old_image(image_filename, _account_name)

        result = client.db.recipes.delete_one({'_id': recipe_id})

        if result.acknowledged:
            if users_to_remove:
                client.db.accounts.update_many({'$or': users_to_remove}, {'$pull': {'favorites': str(recipe_id)}})
            return Response(status=200)
        else:
            abort(500, message='Unable to communicate with database and/or recipe modification failed.')




#search all recipe fields by a string, return recipes with found string
#MAKE SURE THIS WORKS
class Search_Tags(Resource):
    def get(self, tag_str):
        #split string and remove non alphanumeric
        tag_list = [{'tags': re.compile(''.join(c for c in string if c.isalnum()), re.IGNORECASE)} for string in tag_str.split(',')]
        cursor = client.db.recipes.find({'$or': tag_list, 'private': 'False'})
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
api.add_resource(Following_Feed, '/Feed/<num_to_get>', '/Feed')
api.add_resource(Logout, '/Logout')
api.add_resource(Logout2, '/Logout2')
api.add_resource(Refresh, '/Refresh')
api.add_resource(Users, '/Users')
api.add_resource(User, '/User/<username>', '/User')
api.add_resource(Update_Password, '/UpdatePassword')
api.add_resource(Favorites, '/Favorites')
api.add_resource(User_Recipes, '/UserRecipes')
api.add_resource(Recipes, '/Recipes')
api.add_resource(Recipe, '/Recipe/<recipe_id>', '/Recipe')
api.add_resource(Search_Tags, '/SearchTags/<tag_str>')


@app.route('/')
def render_startpage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5000)
