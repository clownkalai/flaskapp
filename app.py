from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def hello_world():
    result="Hi am kalaiyarasan, happy to see you"
    return result
