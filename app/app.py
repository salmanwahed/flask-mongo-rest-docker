from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse
from flask import jsonify, make_response

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/TodoDB"
mongo = PyMongo(app)
api = Api(app)


class TodoList(Resource):
    # Todo list
    def get(self):
        todos = []
        for itm in mongo.db.todos.find():
            itm['id'] = str(itm.pop('_id'))
            todos.append(itm)
        return jsonify(todos)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('priority', choices=('URGENT', 'DEFAULT'))
        args = parser.parse_args()
        insert_result = mongo.db.todos.insert_one(args)
        if insert_result.acknowledged:
            return make_response(jsonify(id=str(insert_result.inserted_id)), 201)
        else:
            return make_response(jsonify(message="Insert Failed"), 200)

    def delete(self):
        delete_result = mongo.db.todos.delete_many({})
        if delete_result.acknowledged:
            return make_response(jsonify(deleted_count=delete_result.deleted_count), 204)
        else:
            return make_response(jsonify(message="Failed Delete"), 204)


api.add_resource(TodoList, '/todos')
