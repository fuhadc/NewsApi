from bson import ObjectId
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from pymongo import MongoClient
import ssl


app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://bayyinadb:AJnQbeg5vuia0rpmnUWOzPdoT8qvyEcXiPkLVh91DTTazjayb9zT1Zr9IrBLSCWRCkvpPtWnPgx5ACDbQV4qOw==@bayyinadb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@bayyinadb@')

db = client.newsapiv
collection = db['mypodcasts']

class HelloWorld(Resource):
    def get(self):
        return {
            "name": "News Connect API",
            "version": 0.1,
        }

class News(Resource):
    def get(self):
        items = db.items.find()
        return jsonify([{'title': item['title'], 'description': item['description'], 'imageUrl': item['imageUrl'] , "articleUrl": item['articleUrl']} for item in items])
        
    def post(self):
        try:
            data = request.get_json()
            item = {'title': data['title'], 'description': data['description'],'imageUrl': data['imageUrl'],'articleUrl':data['articleUrl'] }
            db.items.insert_one(item)
            return make_response(jsonify({'success': 'Item added'}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
    def delete(self):
        try:
            title = request.args.get('title')
            result = db.items.delete_one({'title': title})
            if result.deleted_count == 1:
                return make_response(jsonify({'success': 'Item deleted'}), 200)
            else:
                return make_response(jsonify({'error': 'Item not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
class NewsItem(Resource):
    def put(self, news_title):
        try:
            data = request.get_json()
            result = db.items.update_one({'title': news_title}, {'$set': {'title': data['title'], 'description': data['description'], 'imageUrl': data['imageUrl'], 'articleUrl': data['articleUrl']}})

            if result.modified_count == 1:
                return make_response(jsonify({'success': 'Item updated'}), 200)
            else:
                return make_response(jsonify({'error': 'Item not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
class Podcast(Resource):
    def get(self):
        podcasts = []
        for podcast in collection.find():
            podcasts.append({
                '_id': str(podcast['_id']),
                'title': podcast['title'],
                'description': podcast['description'],
                'image': podcast['image'],
                'audioUrl': podcast['audioUrl']
            })
        return jsonify(podcasts)

    def post(self):
        data = request.get_json()
        podcast = {
            'title': data['title'],
            'description': data['description'],
            'image': data['image'],
            'audioUrl': data['audioUrl']
        }
        result = collection.insert_one(podcast)
        podcast['_id'] = str(result.inserted_id)
        return jsonify(podcast)

class PodcastById(Resource):
    def get(self, id):
        podcast = collection.find_one({'_id': ObjectId(id)})
        if podcast:
            podcast['_id'] = str(podcast['_id'])
            return jsonify(podcast)
        else:
            return make_response(jsonify({'error': 'Podcast not found'}), 404)

    def put(self, id):
        data = request.get_json()
        podcast = {
            'title': data['title'],
            'description': data['description'],
            'image': data['image'],
            'audioUrl': data['audioUrl']
        }
        result = collection.update_one({'_id': ObjectId(id)}, {'$set': podcast})
        if result.modified_count > 0:
            podcast['_id'] = id
            return jsonify(podcast)
        else:
            return make_response(jsonify({'error': 'Podcast not found'}), 404)

    def delete(self, id):
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return make_response('', 204)
        else:
            return make_response(jsonify({'error': 'Podcast not found'}), 404)
        

api.add_resource(Podcast, '/podcasts')
api.add_resource(PodcastById, '/podcasts/<string:id>')
api.add_resource(HelloWorld, '/')
api.add_resource(News,'/News')
api.add_resource(NewsItem,'/NewsItem/<string:news_title>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5556)