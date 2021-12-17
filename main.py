from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pet_api'
app.config['SECRET_KEY'] = 'a828c7af1e3538971a798d84c8f5ac4d'

api = Api(app)
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
migrate = Migrate(app, db)

import api_routes
from middleware import Token_Middleware
app.wsgi_app = Token_Middleware(app.wsgi_app)