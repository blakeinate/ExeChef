# REQUIREMENTS

* need MongoDB installed on system
* need NPM and Angular installed
* need python 2.7 installed
* pip installation recommended to aid in installing of package requirements from requirements.txt
* is is recommended to install these packages in a virtual environment
* after installation of python, you can install all packages needed
* navigate to `/Flask-Backend`
* using the following command `pip install -r requirements.txt`
* To start backend use the following command `python app.py` 
* To run unit tests, run `python app_testing.py` then in a separate terminal run `python unit_tests.py`
* To launch front end, go in to the `/ExeChef-app` directory and run `ng serve`
* the website can be viewed at `localhost:4200`

---
# DATABASE STRUCTURE

## accounts database structure
```
{
    "_id": {
        "$oid": "5a80e397485b9265f90852db"
    }
    'username': 'blakeb',
    'image_name': 'securefilename.jpeg',
    'password': 'mypassword',
    'email': 'blakeb@gmail.com',
    'favorites': ['someid', 'someid'],
    'created' : ['someid', 'someid']
    'following': ['someusername', 'someusername']
    'followers' : ['someusername', 'someusername']
} 
```
## recipes database structure
```
{
    "_id": {
        "$oid": "5a80e397485b9265f90852db"
    }
    "name" : "cool recipe",
    "image_name": "securefilename.jpeg",
    "tags": ["food", "Mexican"],
    "steps" : ["heat oven", "put food in", "eat the food"],
    "author" : "blakeb",
    "description" : "this is the best meal you will ever eat",
    "private" : "True",
    "ingredients" : [{
      "name": "Chicken Broth",
      "amount": "1/2",
      "unit": "Cups"
    }],
    "created_date" : datetime,
    "modified_date" : datetime
    "favorited_count": 10;
}
```
## comments database structure
```
{
    "_id": {
        "$oid": "5a80e397485b9265f90852db"
    }
    'recipe_id': "5a80e397485b9265f90852db",
    'username': "someaccountname",
    'created_date': datetime,
    'body': "this recipe is great stuff!"
    }
}
```
## blacklist database structure (front end should never need to touch this)
```
{
    "token": "jwt_token_string"
}
```
---

# IMAGE STORAGE
## storage location for images is as follows:
* `ExeChef-app/src/assets/images/username/image.jpeg`
* secure filenames will be automatically created.
* if the filename is already in use for the folder, an integer will be prepended to the beginning of the filename. the integer will start with 1 and continue to increase until a
  unique filename is found. The first time a user uploads an image, their individual folder will be created for them.

---

# ENDPOINTS

## create account
#### A POST request to the /User should be made.
### Returns:
```
{
  "data": {
    "user": {
      "_id": {
        "$oid": "5a80e397485b9265f90852db"
      },
      "created": [
        "5a8620a0485b9238269cddfc",
        "5a862149485b9238269cddfd"
      ],
      "favorites": [],
      "password": "datboi",
      "username": "moosey"
    }
  }
}
```
### Requires:
  username, email and password in the following format
```
{
"username":"somename",
"email": "somename@email.com",
"password": "mypassword"
}
```
### Alternate returns:
#### if username is taken, returns:
`422, {'message':'The username provided is already in use.'}`
#### if email taken:
`422, {'message':'The email provided is already in use.'}`
#### if no account name provided:
`422, {'message':'The provided username is invalid.'}`
#### if no email provided:
`422, {'message':'The provided email is invalid.'}`
#### if no password provided:
`422, {'message':'The provided username is invalid.'}`


---

## Login to account
#### A POST request to /Login should be made.
### Returns:
if provided password correct
```
{
  "data": {
    "user": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMTRhOWUwZC1kMGE0LTQ2ZWEtOTZiMy1lMTU3ZGVjY2Y5NzIiLCJleHAiOjE1MTk4NjU5NTksImZyZXNoIjpmYWxzZSwiaWF0IjoxNTE5ODY1MDU5LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTE5ODY1MDU5LCJpZGVudGl0eSI6Im1vb3NleSJ9.qTT-bCVTC07Epe87KoJyvWq5RNKowRgy0PFL1nUKGZA",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlNDI2Njg2ZC05MjU2LTRhYmYtOGFjMi1lMzBjNzZkOTIwOGUiLCJleHAiOjE1MjI0NTcwNTksImlhdCI6MTUxOTg2NTA1OSwidHlwZSI6InJlZnJlc2giLCJuYmYiOjE1MTk4NjUwNTksImlkZW50aXR5IjoibW9vc2V5In0.tHXR6Ebf9AwkXoNj4WRMNjuN6NfGdqDkkQN7xX6AzNk"
      "_id": {
        "$oid": "5a80e397485b9265f90852db"
      },
      "created": [
        "5a8620a0485b9238269cddfc",
        "5a862149485b9238269cddfd"
      ],
      "favorites": [],
      "password": "datboi",
      "username": "moosey"
    },
  }
}
```
### Requires:
  username or email and password in the following format
```
{
"login":"somename (or someemail@gmail.com)",
"password": "mypassword"
}
```
### Alternate returns:
#### if password incorrect, returns:
`422, {'message': 'The current password does not match the password provided.'}`
#### if username/email does not exist, returns:
`422, {'message':'The username/email provided is not associated with an active account.'}`
#### if no username/email provided:
`422, {'message':'Please provide a valid username/email.'}`

---
## update user bio, email, favorite, image, or password
#### A PUT request to /User should be made.
### Returns:
200 if JWT access token provided:
```
{
'data':{
    "user": {
      "_id": {
        "$oid": "5a7cc9db485b921fc97aff9e"
      },
      "created": [],
      "favorites": [],
      "following": [],
      "password": "meepmeep",
      "username": "blakeb"
    }
}
}
```
### Requires:
  JWT Header in the following format:
    `Authorization: Bearer <access token here>`

json data in following format :
note: can provide any combination of these as needed, favorite and following will write over the entire stored list
so provide all the values you want to appear
```
{
"bio": "some bio here",
"email": "blakeb@gmail.com",
"old_password":"password here",
"new_password: "new password here"
"favorites": ["some recipe id", "some recipe id"]
"following": ["some username", "some username:"]
}
```
To send an image, the image holder needs to be named `image`
to remove profile image from the user without providing new image,
you need to pass `'image_name' = 'remove'`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if JWT access token has been revoked:
`{"msg": "Token has been revoked"}`
#### if no bio provided:
`422, {'message': 'No bio provided'}`

#### if any other error occurs, returns:
`500, {'message': 'Unable to communicate with database and/or account modification failed.'}`

---


## refresh access token
#### A POST request to /Refresh should be made.
### Returns:
  if provided JWT refresh token provided:
  ```
  {
    'data':{
        "access_token": "<token here>"
    }
  }
`````
### Requires:
  JWT Header in the following format:
  `Authorization: Bearer <refresh token here>`


### Alternate returns:
#### if JWT refresh token has been revoked:
`{"msg": "Token has been revoked"}`
#### if any other error occurs, returns:
`500, {'message': some exception text}`

---

## Logout of account (revokes/blacklists JWT access token)
#### A DELETE request to /Logout should be made.
### Returns:
200 if provided JWT access token provided and blacklisting success:

### Requires:
JWT Header in the following format:
`Authorization: Bearer <JWT access token here>`


### Alternate returns:
  #### if no access token provided:
    {
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
    }
  #### if blacklisting failed:
    500, {'Unable to communicate with database.'}

---

## Logout of account 2 (revokes/blacklists JWT refresh token, usually want to use this too)
#### A DELETE request to /Logout2 should be made.
### Returns:
    200 if provided JWT refresh token provided and blacklisting success:


### Requires:
JWT Header in the following format:
`Authorization: Bearer <refresh token here>`


### Alternate returns:
  #### if JWT refresh token has been revoked:
    {"msg": "Token has been revoked"}
  #### if blacklisting failed:
    500, {'Unable to communicate with database.'}

---

## get current user
#### A GET request to the /User should be made.
### Returns: 
if valid JWT:
```
{
    "user": {
      "_id": {
        "$oid": "5a7cc9db485b921fc97aff9e"
      },
      "created": [],
      "favorites": [],
      "password": "meepmeep",
      "username": "blakeb"
    }
}
```
### Requires: 
JWT Header in the following format:
`Authorization: Bearer <access token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if blacklisting failed:
`400, {'message':'No user found associated with provided access token.'}`

---

## get following feed for user
#### A GET request to the /Feed/<num_to_get> should be made. if no <num_to_get> provided, defaults to 10
### Returns: 
if valid JWT, returns num_to_get public recipes that are most recent from the users followers
if no JWT provided, returns num_to_get recent public recipes from all users:
```            
{
  "recipes": [
    {
      "_id": {
        "$oid": "5a7cdade485b925737ef6ef5"
      },
      "author": "BlakeB",
      "category": "great stuff food",
      "created_date": {
        "$date": 1518110334999
      },
      "description": "this isi the best ting you will ever eat",
      "ingredients": [
        {
          "amount": "tree-fitty",
          "name": "great stuff",
          "unit": "pounds"
        }
      ],
      "modified_date": {
        "$date": 1518110334999
      },
      "name": "great stuff recipe",
      "private": "True",
      "steps": [
        "do cool stuff",
        "do more cool stuff",
        "eat that stuff"
      ],
      "user": {
          "_id": {
            "$oid": "5ad00a0869438c029e5d3a4f"
          },
          "bio": "1SBDT1CEZE",
          "username": "testuser"
        }
    },
    {
      "_id": {
        "$oid": "5a7ce708485b9274f77a215a"
      },
      "author": "BlakeB",
      "category": "great stuff food",
      "created_date": {
        "$date": 1518113448462
      },
      "description": "this isi the best ting you will ever eat",
      "ingredients": [
        {
          "amount": "tree-fitty",
          "name": "great stuff",
          "unit": "pounds"
        }
      ],
      "modified_date": {
        "$date": 1518113448462
      },
      "name": "great stuff recipe",
      "private": "True",
      "steps": [
        "do cool stuff",
        "do more cool stuff",
        "eat that stuff"
      ],
      "user": {
          "_id": {
            "$oid": "5ad00a0869438c029e5d3a4f"
          },
          "bio": "1SBDT1CEZE",
          "username": "testuser"
        }
    }
  ]
}
```
### Requires: 
JWT Header in the following format:
`Authorization: Bearer <access token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### any other error:
`500, {'message':'some error here'}`

---

## get user by username without sensitive information
#### A GET request to the /User/<username> should be made.

### Returns: 
 if valid JWT:
```
{
"user": {
  "_id": {
    "$oid": "5a7cc9db485b921fc97aff9e"
  },
  "created": [],
  "favorites": [],
  "username": "blakeb",
  "following": "True"
}
}
```
  NOTE: the "following" option will only be passed if a JWT header is also provided
  this will compare the current logged in users following list to the username provided in the URL
### Requires: 
Optional JWT Header in the following format:
`Authorization: Bearer <access token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
####if blacklisting failed:
`400, {'message':'No user found associated with provided access token.'}`

---

## create a recipe
#### A POST request to the /Recipe should be made.
### Returns: 

recipe id in the following format:
```
{
  "id": "5a7ce708485b9274f77a215a"
}
```
### Requires: 
recipe information in the following format:
(note: author added from username associated with JWT)
```      
{
"name": "good recipe",
"tags": ["food"],
"steps" : ["do cool stuff", "do more cool stuff", "eat it!"],
"description": "this is the best ting you will ever eat",
"private": "True",
"ingredients": [{"name":"goodgood", "amount":"tree-fitty", "unit":"pounds"}]
}
```
###OPTIONAL:

To send an image, the image holder needs to be named `image`

Header in the following format:
`Authorization: Bearer <access token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if missing fields:
`422, {'message':'Some required fields were not provided.'}`

---

## update a recipe
#### A PUT request to the /Recipe should be made.
### Returns:
200
### Requires: 
recipe information in the following format (fields besides id can be missing, only updates fields provided):
```
{
"id" : "5a7ce708485b9274f77a215a",
"steps" : ["do cool stuff", "do more cool stuff", "eat it!"],
"description": "this is the best ting you will ever eat",
"private": "True",
"ingredients": [{"name":"goodgood", "amount":"tree-fitty", "unit":"pounds"}]
}
```

Header in the following format:
`Authorization: Bearer <access token here>`


To send an image, the image holder needs to be named `image`
to remove profile image from the user without providing new image,
you need to pass `'image_name' = 'remove'`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if update was not successful:
`500, {'message':'Unable to communicate with database and/or recipe modification failed.'}`

---

## get a single recipe
#### A GET request to the /Recipe/<recipe_id> should be made.
### Returns: 
a recipe in the following format:
```
{
'data':{
    "recipe": {
      "_id": {
        "$oid": "5a7cdade485b925737ef6ef5"
      },
      "author": "BlakeB",
      "tags": ["food"],
      "image_name": "securefilename.jpeg",
      "created_date": {
        "$date": 1518110334999
      },
      "description": "this is the best ting you will ever eat",
      "ingredients": [
        {
          "amount": "tree-fitty",
          "name": "great stuff",
          "unit": "pounds"
        }
      ],
      "modified_date": {
        "$date": 1518110334999
      },
      "name": "great stuff recipe",
      "private": "True",
      "steps": [
        "do cool stuff",
        "do more cool stuff",
        "eat that stuff"
      ],
      "in_favorites": True #will only show up if JWT provided,
      "user": {
          "_id": {
            "$oid": "5ad00a0869438c029e5d3a4f"
          },
          "bio": "1SBDT1CEZE",
          "username": "testuser"
      }
    }
}
}
```
### Requires: 
a recipe_id to be passed at the end of the route
### Optional: 
JWT Header in the following format:
`Authorization: Bearer <access token here>`
This is required if a private recipe needs to be accessed.
The provided token must be associated with the author of recipe.
Optional: If JWT provided a `in_favorites` boolean item will be returned with the recipe
### Alternate returns:
#### if id is incorrect:
`400, {'message':'No recipe found with the provided recipe ID.'}`
#### if recipe is private and author does not match current user:
`403, {'message':'Private recipe is owned by another user.'}`

---

## get users created recipes
#### A GET request to the /Recipe/Created/<username>/<num_to_get> or /Recipe/Created/<num_to_get> should be made.
    username and num_to_get are optional parameters, without username, gets logged in users recipes, this requires JWT
### Returns: 
list of recipes in the following format:
```
{
'data':{
    "recipes": [
      {
        "_id": {
          "$oid": "5a7cdade485b925737ef6ef5"
        },
        "author": "BlakeB",
        "tags": ["food"],
        "created_date": {
          "$date": 1518110334999
        },
        "description": "this is the best ting you will ever eat",
        "ingredients": [
          {
            "amount": "tree-fitty",
            "name": "great stuff",
            "unit": "pounds"
          }
        ],
        "modified_date": {
          "$date": 1518110334999
        },
        "name": "great stuff recipe",
        "private": "True",
        "steps": [
          "do cool stuff",
          "do more cool stuff",
          "eat that stuff"
        ],
        "user": {
          "_id": {
            "$oid": "5ad00a0869438c029e5d3a4f"
          },
          "bio": "1SBDT1CEZE",
          "username": "testuser"
        }

      }
    ]
}
}
```
### Requires: 
JWT Header in the following format:
`Authorization: Bearer <access token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if access token does not relate to active user:
`400, {'message':'No user found associated with provided access token.'}`

---

## get users favorite recipes
#### A GET request to the /Recipe/Favorites/<username>/<num_to_get> or /Recipe/Favorites/<num_to_get> should be made.
username and num_to_get are optional parameters, without username, gets logged in users recipes, this requires JWT
### Returns: 
list of recipes in the following format:
```
{
'data':{
    "recipes": [
      {
        "_id": {
          "$oid": "5a7cdade485b925737ef6ef5"
        },
        "author": "BlakeB",
        "tags": ["food"],
        "created_date": {
          "$date": 1518110334999
        },
        "description": "this is the best ting you will ever eat",
        "ingredients": [
          {
            "amount": "tree-fitty",
            "name": "great stuff",
            "unit": "pounds"
          }
        ],
        "modified_date": {
          "$date": 1518110334999
        },
        "name": "great stuff recipe",
        "private": "True",
        "steps": [
          "do cool stuff",
          "do more cool stuff",
          "eat that stuff"
        ]
        "user": {
          "_id": {
            "$oid": "5ad00a0869438c029e5d3a4f"
          },
          "bio": "1SBDT1CEZE",
          "username": "testuser"
        }
      }
    ]
}
}
```
### Requires: 
JWT Header in the following format:
`Authorization: Bearer <token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
####if access token does not relate to active user:
`400, {'message':'No user found associated with provided access token.'}`

---

## add comment for a recipe
#### A POST request to the /Recipe/<recipe_id>/comments should be made.
### Returns: 
Status code 200 and
```
{ 'comment':
    {
        "_id": {
            "$oid": "5a80e397485b9265f90852db"
        }
        'recipe_id': "5a80e397485b9265f90852db",
        'username': "someaccountname",
        'created_date': datetime,
        'body': "this recipe is great stuff!"
        'user': {
          '_id': {
            '$oid': '5a7cc9db485b921fc97aff9e'
          },
          'username': 'blakeb',
          'image_name': 'someimage.jpeg'
        }
    }
}
```
### Requires: 
JWT access token and following format to send comment
Header in the following format:
`Authorization: Bearer <token here>`
    
### Alternate returns:
#### if no text in comment:
`400, {'message'='No comment text provided.'}`
#### if create was not successful:
`500, {'message':'Unable to communicate with database and/or recipe modification failed.'}`

---

## get comments for a recipe
#### A GET request to the /Recipe/<recipe_id>/comments should be made.
### Returns: 
comments in following format
```
{'comments':
    [{
    "_id": {
        "$oid": "5a80e397485b9265f90852db"
    }
    'recipe_id': "5a80e397485b9265f90852db",
    'username': "someaccountname",
    'created_date': datetime,
    'body': "this recipe is great stuff!"
    'user': {
      '_id': {
        '$oid': '5a7cc9db485b921fc97aff9e'
      },
      'username': 'blakeb',
      'image_name': 'someimage.jpeg'
    }

    }]
}
```
### Requires: 
`recipe_id` passed in route

---

## delete comment for a recipe
#### A DELETE request to the /Recipe/comments/<comment_id> should be made.
### Returns: 
200
### Requires: 
JWT access token and following format to send comment
Header in the following format:
`Authorization: Bearer <token here>`

Also requires a `comment_id` passed in route

### Alternate returns:
#### if comment not owned by user or doesn't exist:
`403, {'message'='Comment owned by another user or does not exist.'}`
#### if create was not successful:
`500, {'message':'Unable to communicate with database and/or recipe modification failed.'}`

## delete a recipe
#### A DELETE request to the /Recipe/<recipe_id> should be made.
### Returns: 
200
### Requires: 
The JWT token provided is associated with the account that owns the recipe.

Header in the following format:
`Authorization: Bearer <token here>`

### Alternate returns:
#### if no access token provided:
```
{
"description": "Request does not contain an access token",
"error": "Authorization Required",
"status_code": 401
}
```
#### if delete was not successful:
`500, {'message':'Unable to communicate with database and/or recipe modification failed.'}`
#### if user not owner of the recipe:
`403, {'message':'Recipe is owned by another user. Modifications are not allowed.'}`

---

## retrieve recipes by tag
#### A GET request to the /SearchTags/<tag_str>/<num_to_get> should be made.
tags should be separated by '&'
## Returns: 
a list of recipes containing any of the searched tags in the following format:
```
{
    'data':{
        "recipes": [
          {
            "_id": {
              "$oid": "5a7cdade485b925737ef6ef5"
            },
            "author": "BlakeB",
            "tags": ["food"],
            "created_date": {
              "$date": 1518110334999
            },
            "description": "this is the best ting you will ever eat",
            "ingredients": [
              {
                "amount": "tree-fitty",
                "name": "great stuff",
                "unit": "pounds"
              }
            ],
            "modified_date": {
              "$date": 1518110334999
            },
            "name": "great stuff recipe",
            "private": "True",
            "steps": [
              "do cool stuff",
              "do more cool stuff",
              "eat that stuff"
            ]
          }
        ]
    }
}
```
### Requires: 
a tag_string to be passed at the end of the route
The tag string should be a list of tags separated by commas "`,`"
