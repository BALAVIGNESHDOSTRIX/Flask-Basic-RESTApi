from flask import Flask,request
from flask_restful import Resource,Api
import pymongo as mon
import json
from bson import json_util

app = Flask(__name__)
api = Api(app)

myclient = mon.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dostrixDB"]
mycol = mydb['dostrixCollection']

class MongoTest(Resource):
    
    def post(self):
        json_data = request.get_json()
        mydict = {'name' : json_data['name'],'email' : json_data['email']}
        x = mycol.insert_one(mydict)
        return {"result" : str(x.inserted_id)  + ' Successfully Inserted'}

    def get(self):
       name = request.args.get('name')
       doc =  mycol.find({"name" : name})
       res = []
       for x in doc:
           res.append(x)
       return json.loads(json_util.dumps(res))


    def put(self):
        json_data = request.get_json()
        myquery = { "name": json_data['find_name'] }
        newvalues = {"$set" : {"name" : json_data['name']}}
        mycol.update_one(myquery,newvalues)
        res = []
        for x in mycol.find():
            res.append(x)
        return json.loads(json_util.dumps(res))
    
    def delete(self):
        json_data = request.get_json()
        myquery = {"name" : json_data['name']}
        mycol.delete_one(myquery)
        return {"result" : "Successfully Deleted the Record"}


api.add_resource(MongoTest,'/mongo',methods=['GET', 'POST','PUT','delete'])

if __name__ == '__main__':
    app.run(debug=True)