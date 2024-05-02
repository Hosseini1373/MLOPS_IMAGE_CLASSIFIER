from flask import Flask
from flask_cors import CORS
from flask import request
from pymongo import MongoClient
from flask import jsonify
from io import BytesIO
from bson.objectid import ObjectId
import base64
import datetime
import time
import requests
import json
import public_ip as ipf


# Create a buffer to hold the bytes
buf = BytesIO()

#mongodb+srv://zgnmgb:<password>@imagestorage.xycpeuy.mongodb.net/?
#client = MongoClient('mongodb://192.168.56.1:27017/')
client = MongoClient('mongodb+srv://zgnmgb:1n4QdMljxUihbJrX@imagestorage.xycpeuy.mongodb.net/?')
db = client["MLOPS"]
app = Flask(__name__)
CORS(app)
ip = ipf.get()+':443' #"34.32.24.204:443"

@app.route('/')
def index():
    return 'Hallo'
    
@app.route('/save/', methods=['POST'])
def insert_image():
    im = request.get_data()
    t_orig = time.time()
    t = datetime.datetime.fromtimestamp(t_orig).strftime('%c')
    animal = requests.post(f"http://{ip}/inference/classify", json={'image_b64':base64.b64encode(im).decode("utf-8")})
    print(animal)
    res = db['MLOPS'].insert_one({
        "picture":im,
        "timestamp":t,
        "torig":t_orig,
        "prediction":animal.content.decode("utf-8")
    })
    
    return jsonify({"id": str(res.inserted_id),'class':animal.content.decode("utf-8")})

@app.route('/data/<id>', methods=['GET'])
def get_data(id):
    images = db['MLOPS'].find_one(ObjectId(id))
    images = base64.b64encode(images['picture']).decode("utf-8")
    return jsonify([images])

@app.route('/save/<id>', methods=['Post'])
def insert_trueval(id):
    animal = request.get_data().decode('ascii')
    db['MLOPS'].update_one({'_id' : ObjectId(id)},{'$set' : {'breed' :  animal,'trained':False}})
    return jsonify({"res":"success"})
    


if __name__ == '__main__':
        app.run(
        host="0.0.0.0",
        debug=True,
        passthrough_errors=True,
        use_debugger=False,
        use_reloader=True,
    )