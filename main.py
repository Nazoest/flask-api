#Rules of a REST API
#1.Data is transfered from one application to another in key:alue pairs called JSON.
#2.You have to define a route/URI.
#3.You define a method e.g GET,POST,PUT,PATCH,DELETE
#4. You have to define a status code for the app receiving the data to know how to handle the data e.g 200,404,403

from datetime import timedelta
from flask import Flask,jsonify,request
from models import db,Product,User,Sales,Purchases
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS

app=Flask(__name__)
#to be complete with sql alchemy
# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nazo@localhost:5432/flaskapi'
db.init_app(app)
CORS(app)

jwt=JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=30)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'  

myproducts=[]
mysales=[]
myusers=[]

@app.route("/",methods=["GET"])
def home():
    return({"Flask API" : "1.0"}),200

@app.route("/api/register",methods=["POST"])
def register():
    data=request.get_json()
    new_user=User(
        username=data["username"],
        email=data["email"],
        password=data["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    data["id"]=new_user.id
   
    token=create_access_token(identity=data["email"])
    return jsonify({"token":token}),201



@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    usr = User.query.filter_by(email=data["email"], password=data["password"]).first() 
    if usr is None:
            error = {"error": "Invalid email or password"}
            return jsonify(error), 401
    else:
            token = create_access_token(identity = data["email"])
            return jsonify({"token": token}), 200 



@app.route("/products",methods=["GET","POST"])
@jwt_required()
def products():
    if request.method=="GET":
        myproducts=Product.query.all()
        products_list=[]
        for product in myproducts:
            products_list.append({
                "id": product.id,
                "name": product.name,
                "buying_price": product.buying_price,
                "selling_price": product.selling_price
            })

        return jsonify(products_list),200
    elif request.method=="POST":
        data=request.get_json()
        new_product=Product(
            name=data["name"],
            buying_price=data["buying_price"],
            selling_price=data["selling_price"]
        )
        db.session.add(new_product)
        db.session.commit()
        data["id"]=new_product.id

        return jsonify({"Message":"Success"}),201
    else:
        error={"error":"Method not allowed"}
        return jsonify(error),405
    
@app.route("/sales", methods=["GET","POST"] )
@jwt_required()
def sales():
    if request.method == "GET":
        mysales = Sales.query.all() 
        sales_list = []
        for sale in mysales:
            sales_list.append({
                "id": sale.id,
                "product_id": sale.product_id,
                "quantity": sale.quantity,
                "created_at": sale.created_at
            })   
        return jsonify(sales_list), 200
    
    elif request.method == "POST":
        data = request.get_json()
        new_sale=Sales(
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        db.session.add(new_sale)
        db.session.commit()
        data['id'] = new_sale.id
        data['created_at'] = new_sale.created_at
        return jsonify({"message": "Sale recorded successfully"}), 201
    
    else:
        error = {"message": "Method not allowed"}
        return jsonify(error), 405

@app.route("/purchases", methods=["GET","POST"] )
@jwt_required()
def purchases():
    if request.method == "GET":
        mypurchases = Purchases.query.all() 
        purchases_list = []
        for purchase in mypurchases:
            purchases_list.append({
                "id": purchase.id,
                "product_id": purchase.product_id,
                "stock_quantity": purchase.stock_quantity,
                "created_at": purchase.created_at
            })   
        return jsonify(purchases_list), 200
    
    elif request.method == "POST":
        data = request.get_json()
        new_purchase=Purchases(
            product_id=data['product_id'],
            stock_quantity=data['stock_quantity']
        )
        db.session.add(new_purchase)
        db.session.commit()
        data['id'] = new_purchase.id
        data['created_at'] = new_purchase.created_at
        return jsonify({"message": "Purchase recorded successfully"}), 201
    
    else:
        error = {"message": "Method not allowed"}
        return jsonify(error), 405



if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)
