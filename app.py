from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)



def dbconnection():
    connection_string = "mongodb+srv://kalaiyarasan:kjqYYemV2V0R5RE6@cluster0.7g1bffo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    client = MongoClient(connection_string)
    db = client["Crud_2023"]

@app.route('/')
def hello_world():
    db = dbconnection()
    col = db["userInfo"]
    cursor = col.find({},{'_id':0})
    result = [item for item in cursor]
    return 'Hello, World!'
