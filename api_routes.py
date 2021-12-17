from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse
from flask.views import MethodView
from models import User, Pet
from main import app, api, db, marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema
import jwt
#---------------------------------------------------------------------------
class Hello(Resource): 
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify(
            {
                'message': 'You can route to these 2 links.',
                'links': {'users': '/users', 'pets':'/pets'}
            }
        )

class Square(Resource):
  
    def get(self, num):
        return jsonify({'square': num**2})

# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')
#---------------------------------------------------------------------------
# for marshmallow
class userSchema(marshmallow.Schema):
    class Meta:
        fields = ['id', 'name', 'number', 'category', 'email', 'username', 'password']
        model = User

user_schema = userSchema() # for POST & Filtering data
users_schema = userSchema(many=True) # for multiple data/GET req

class UserView(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        new_user = User(
            name = request.json['name'],
            number = request.json['number'],
            category = request.json['category'],
            email = request.json['email'],
            username = request.json['username'],
            password = request.json['password']
        )
        db.session.add(new_user)
        db.session.commit()

        # token = jwt.encode({'alog':'HS256', 'name':new_user.email}, app.config['SECRET_KEY'])

        return user_schema.dump(new_user)
        # return jsonify(token)
api.add_resource(UserView, '/users')

class specificUser(Resource):
    def get(self, id):
        specific_user = User.query.get(id)
        if not specific_user:
            abort(404, message='user not found')
        
        token = jwt.encode({'alog':'HS256', 'name':specific_user.email}, app.config['SECRET_KEY'])
        # return user_schema.dump(specific_user)
        return jsonify(token)

    def put(self, id):
        specific_user_update = User.query.get(id)
        if not specific_user_update:
            abort(404, message='user not found')
        specific_user_update.name = request.json['name']
        specific_user_update.number = request.json['number']
        specific_user_update.category = request.json['category']
        specific_user_update.email = request.json['email']
        specific_user_update.username = request.json['username']
        specific_user_update.password = request.json['password']
        db.session.commit()
        return user_schema.dump(specific_user_update)

    def delete(self, id):
        specific_user_delete = User.query.get(id)
        if not specific_user_delete:
            abort(404, message='user not found')
        db.session.delete(specific_user_delete)
        db.session.commit()
        return user_schema.dump(specific_user_delete)
api.add_resource(specificUser, '/user/<int:id>')
#----------------------------------------------------------------------------
class petSchema(SQLAlchemySchema):
    class Meta:
        fields = ['id', 'name', 'pet_type', 'age', 'user']
        model = Pet

pet_schema = petSchema()
pets_schema = petSchema(many=True)

class PetView(Resource):
    def get(self):
        pets = Pet.query.all()
        # print("pets", pets)
        return pets_schema.dump(pets)

    def post(self):
        new_pet = Pet(
            name = request.json['name'],
            pet_type = request.json['pet_type'],
            age = request.json['age'],
            user = request.json['user'],
        )
        db.session.add(new_pet)
        db.session.commit()
        return pet_schema.dump(new_pet)
# breakpoint()
api.add_resource(PetView, '/pets')

class specificPet(Resource):
    def get(self, id):
        specific_pet = Pet.query.get(id)
        if not specific_pet:
            abort(404, message='pet not found')
        return pet_schema.dump(specific_pet)

    def put(self, id):
        specific_pet_update = Pet.query.get(id)
        if not specific_pet_update:
            abort(404, message='pet not found')
        specific_pet_update.name = request.json['name']
        specific_pet_update.pet_type = request.json['pet_type']
        specific_pet_update.age = request.json['age']
        specific_pet_update.user = request.json['user']
        db.session.commit()
        return pet_schema.dump(specific_pet_update)
    
    def delete(self, id):
        specific_pet_delete = Pet.query.get(id)
        if not specific_pet_delete:
            abort(404, message='pet not found')
        db.session.delete(specific_pet_delete)
        db.session.commit()
        return pet_schema.dump(specific_pet_delete)
api.add_resource(specificPet, '/pet/<id>')
#-------------------------------------------------------------------------
