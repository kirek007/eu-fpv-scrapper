import json
import re


import pymongo
from bson import json_util
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_prefixed_env()

mongoUrl = app.config.from_envvar('MONGO_URL', True)

app.config["MONGO_URI"] = mongoUrl if mongoUrl else "mongodb://marek:abrakadabra12@127.0.0.1:27017/fpvScrapper?authSource=admin"
# app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app)
api = Api(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def home_results():
    phrase = request.args.get("phrase")
    if phrase is None:
        return render_template("index.html")

    regx = re.compile(phrase, re.IGNORECASE)
    things = mongo.db.products.aggregate([
        {"$match": {"$text": {"$search": phrase}}},
        {"$match": {"can_buy": True}},
        {"$project": {"_id": False, "name": True, "price": True, "url": True, "category": True, "score": { "$meta": "textScore" }}},
        {"$sort": {"score": pymongo.DESCENDING}},
        {"$limit": 20},

    ])

    res = json.loads(json_util.dumps(things))

    return render_template("index.html", results=res)

if __name__ == '__main__':
    app.run(debug=True)
