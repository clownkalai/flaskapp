from flask import Flask,render_template, request, redirect, url_for,jsonify,abort
from datetime import datetime, timedelta
from user_functions import *
from dbfunctions import *

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7' 
jwt = JWTManager(app)


@app.route('/')
def hello_world():
    result="Hi am kalaiyarasan, happy to see you"
    return result

@app.route('/users', methods=['GET'])
def get_allUsers():
    user_list = find_all_collection("userInfo")
    return user_list
