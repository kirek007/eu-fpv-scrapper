import json
import re


import pymongo
from bson import json_util
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_prefixed_env()
# app.config["MONGO_URI"] = app.config.from_envvar('MONGO_URL')
# app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app)
api = Api(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def home_results():
    phrase = request.args.get("phrase")
    regx = re.compile(phrase, re.IGNORECASE)
    things = mongo.db.products.find(
        {"can_buy": True, "name": regx},
        {"_id": False, "name": True, "price": True, "url": True, "category": True}
    ).sort("price", pymongo.ASCENDING)
    res = json.loads(json_util.dumps(things))

    return render_template("index.html", results=res)

if __name__ == '__main__':
    app.run(debug=True)
