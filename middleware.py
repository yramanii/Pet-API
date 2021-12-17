from werkzeug.wrappers import Request, Response

from flask import request, jsonify

from models import User
from main import app

import jwt
#----------------------------------------------------------------------------
class Token_Middleware():

    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        breakpoint()
        req = Request(environ)

        with app.app_context():
            if req.method=='GET' and req.path=='/users':
                pass
            elif req.method=='GET' and req.path=='/user/':
                pass
            else:
                token = req.headers['tokens']

                if not token:
                    return jsonify({"Message":"Token is required."})
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                    user = User.query.filter_by(email = data['name']).first()
                except:
                    return jsonify({"Message": "Enter a valid token."})
            
            return self.app(environ, start_response)
        
        return Response(environ, start_response)