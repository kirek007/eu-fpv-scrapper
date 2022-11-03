import json
import os
import pprint
import re


import pymongo
from bson import json_util
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_prefixed_env()

app.config["MONGO_URI"] = os.getenv('MONGO_URL', "mongodb://marek:abrakadabra12@127.0.0.1:27017/fpvScrapper?authSource=admin")
# app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app)
api = Api(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def home_results():
    phrase = request.args.get("phrase","")
    smartSerach = bool(request.args.get("smart", False))
    debug = bool(request.args.get("debug", False))
    if not phrase:
        return render_template("index.html")

    if smartSerach:
        agg_pipeline = [
            {"$match": {"$text": {"$search": phrase}}},

            {"$match": {"can_buy": True}},
            {"$project": {"_id": False, "shop": True, "name": True, "price": True, "url": True, "category": True, "score": { "$meta": "textScore" }}},
            {"$sort": {"score": pymongo.DESCENDING}},
            {"$limit": 20},
            {"$match": {"score": {"$gt": 0.5}}},

        ]
        things = mongo.db.products.aggregate(agg_pipeline)
        # explain_output = mongo.db.command('aggregate', 'products', pipeline=agg_pipeline, explain=True)
        # pprint.pprint(explain_output)
        res = json.loads(json_util.dumps(things))
    else:
        regx = re.compile(phrase, re.IGNORECASE)
        things = mongo.db.products.find(
            {"can_buy": True, "name": regx},
            {"_id": False, "name": True, "price": True, "url": True, "category": True, "shop": True}
        ).sort("price", pymongo.ASCENDING).limit(20)
        res = json.loads(json_util.dumps(things))

    return render_template("index.html", results=res, debug=debug, phrase=phrase, smart=smartSerach)


if __name__ == '__main__':
    app.run(debug=True)
