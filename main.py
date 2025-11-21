#Rules of a REST API
#1.Data is transfered from one application to another in key:alue pairs called JSON.
#2.You have to define a route/URI.
#3.You define a method e.g GET,POST,PUT,PATCH,DELETE
#4. You have to define a status code for the app receiving the data to know how to handle the data e.g 200,404,403

from flask import Flask,jsonify,request

app=Flask(__name__)
#to be complete with sql alchemy
myproducts=[]
mysales=[]
myusers=[]

@app.route("/",methods=["GET"])
def home():
    return({"Flask API" : "1.0"}),200

@app.route("/products",methods=["GET","POST"])

def products():
    if request.method=="GET":
        return jsonify(myproducts),200
    elif request.method=="POST":
        data=request.get_json()
        myproducts.append(data)
        return jsonify({"Message":"Success"}),201
    else:
        error={"error":"Method not allowed"}
        return jsonify(error),405


app.run(debug=True)
