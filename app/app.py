#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound


from models import db, Restaurant,Pizza,Restaurant_pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api= Api(app)

@app.errorhandler(NotFound)
def handle_not_found(e):
    response= make_response("NotFound: The requested resource not found", 404)
    return response

@app.route('/')
def home():
    return 'Hello'

class Restaurants(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Restaurant.query.all()]
        response= make_response(jsonify(response_dict), 200)
        return  response

class Pizz(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Pizza.query.all()]
        if len(response_dict)==0:
            response= make_response("Record not found", 404)
            return response
        else :
            response= make_response(jsonify(response_dict), 200)
            return response


#Api routes
api.add_resource(Restaurants, '/restaurants')
api.add_resource(Pizz, '/pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
