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

@app.route('/register',methods=['POST'])
def user_register():
    data = request.json
    hash_password = get_password_hash(str(data.get("password")))
    user_data ={
            "first_name":data.get("first_name"),
            "last_name":data.get("last_name"),
            "email":data.get("email"),
            "password":hash_password,
        }
    try:
        #insert the user in db
        registered_user = save_collection("userInfo",user_data)
        if registered_user.acknowledged:
            response = {
                    "status" :"success",
                    "message" : "User was registered successfully."
            }
            status_code =201
            return response,status_code
        else:
            response = {
                    "status" :"Failed",
                    "message" : "User  registeration failed."
            }

            return response
    except Exception as e:
            return "Something went wrong."  ,500  
@app.route('/login', methods=['POST'])
def login():
    data =  request.json
    user = authenticate_user(data.get("email"), data.get("password"))

    if not user:
        abort(401) 

    user_details= getUserByEmailId(data.get("email"))

    
    try:
        expiration_time = timedelta(1800)
 
        access_token = create_access_token(identity=user[0]["email"], expires_delta=expiration_time)

    except Exception as e:
        abort(401)

    response ={
        "status":"success",
        "access_token": access_token,
        "token_type": "bearer",
        "users":user_details
    }
    return response

@app.route('/template', methods=['POST'])
@jwt_required()
def create_template():
    current_user = get_jwt_identity()
    if current_user is None:
            abort(401)
        
    data = request.json
    template = {
            'templateId':gentemplateId(),
            'created_by':current_user,
            'template_name': data.get('template_name'),
            'subject': data.get('subject'),
            'body': data.get('body')
        }

    saveTemplate = save_collection('templates',template)
    if saveTemplate.acknowledged:
        response = {
                    "status" :"success",
                    "message" : "Template saved successfully."
            }
       
        return response,201
    else:
        response = {
                    "status" :"Failed",
                    "message" : "Failed to save template."
        }
        return response

#Get All Template
@app.route('/template', methods=['GET'])
@jwt_required()
def all_templates():
    current_user = get_jwt_identity()
    if current_user is None :
            abort(401)

    collection ="templates"
    arr={"created_by":current_user}
    all_templates = find_in_collection(collection,arr)
    return all_templates

#get single templates
@app.route('/template/<templateid>', methods=['GET'])
@jwt_required()
def get_Singletemplate(templateid:str):
    current_user = get_jwt_identity()
    if current_user is None :
            abort(401)

    arr = {"templateId" : int(templateid),"created_by":current_user}

    all_templates = find_one_in_collection("templates",arr)
    return all_templates

#update template
@app.route('/template/<templateid>', methods=['PUT'])
@jwt_required()
def update_template(templateid:str):
    current_user = get_jwt_identity()
    if current_user is None :
            abort(401)
    data =request.json
    update_template = {
           
            'template_name': data.get('template_name'),
            'subject': data.get('subject'),
            'body': data.get('body')
        }

    arr = {"templateId" : int(templateid),"created_by":current_user}
    
    check_data = find_in_collection("templates",arr)
    
    if check_data == []:
        response ={
                    "status" :"Failed",
                    "message" : "Your Template Not Found"
        }
        return response

    set_template = {'$set':update_template}

    update_collection("templates",arr,set_template)
    response = {
                    "status" :"success",
                    "message" : "Template updated successfully"
        }
    return response

#delete template
@app.route('/template/<templateid>', methods=['DELETE'])
@jwt_required()
def delete_template(templateid:str):

    current_user = get_jwt_identity()
    if current_user is None :
            abort(401)

    arr = {"templateId" : int(templateid),"created_by":current_user}
    check_data = find_in_collection("templates",arr)
    if check_data == []:
        response ={
                    "status" :"Failed",
                    "message" : "Your Template Not Found"
        }
        return response

    drop_collection("templates",arr)
    response = {
                    "status" :"Sucess",
                    "message" : "Template deleted successfully"
        }
    return response

@app.errorhandler(401)
def unauthorized_error_handler(error):
    # Create a custom response object with custom headers
    unauthorized_headers = {"WWW-Authenticate": "Bearer"}
    response = jsonify(error="Could not validate credentials")
    response.status_code = 401
    for header, value in unauthorized_headers.items():
        response.headers[header] = value
    return response
