from pymongo import MongoClient



def dbconnect():
        #mongodb connection string
        connection_string = "mongodb+srv://kalaiyarasan:kjqYYemV2V0R5RE6@cluster0.7g1bffo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

        # Create a MongoDB client
        client = MongoClient(connection_string)
        db = client["Crud_2023"]
        return db


def find_latest_in_collection_sort(collection,sort_arr):

        db = dbconnect()
        coll = db[collection]
        cursor = coll.find().sort(sort_arr).limit(1)
        result = [item for item in cursor]
        return result

def find_all_collection(collection):
        db = dbconnect()
        col = db[collection]
        cursor = col.find({},{'_id':0})
        result = [item for item in cursor]
        return result 

def find_one_in_collection(collection,arr):
        
        db=dbconnect()
        col = db[collection]
        cursor = col.find(arr,{'_id':0})
        result = [item for item in cursor]
        
        return result


def save_collection(collection,arr):

        db = dbconnect()
        coll = db[collection]
        data = coll.insert_one(arr)
        return data

def find_and_filter(collection,arr,ary):
        db = dbconnect()
        coll = db[collection]
        cursor = coll.find(arr,ary)
        result = [item for item in cursor]
        return result

def find_in_collection(collection,arr):
        
        db = dbconnect()
        coll = db[collection]
        cursor = coll.find(arr,{'_id':0})
        result = [item for item in cursor]
        
        return result

def update_collection(collection,arr,ary):
      
        db = dbconnect()
        coll = db[collection]
        data = coll.update_one(arr,ary)
        return data

def drop_collection(collection,arr):
        db = dbconnect()
        coll = db[collection]
        data = coll.delete_one(arr)
        return data        
