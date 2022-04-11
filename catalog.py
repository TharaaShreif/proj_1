from flask import Flask, json
from flask import request
from flask import jsonify
from flask.sessions import NullSession
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.fields import Integer
from marshmallow import Schema

#init app
app = Flask(__name__)
#init marshmallow
ma = Marshmallow(app)

#For Database "BooksInfo_DB" we filled it by terminal 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BooksInfo_DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#create DB
class Catalog_Server_DB(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(500))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    topic = db.Column(db.String(500))
     

    def __init__(self,id,title,quantity,price,topic):
        self.id=id
        self.title=title
        self.quantity=quantity
        self.price=price
        self.topic=topic
#dectionary
book={}

#frontend
#1:search,get all books that have spicific topic
@app.route("/search/<topic>", methods=['GET'])
def search_by_topic(topic):
    book = Catalog_Server_DB.query.with_entities(Catalog_Server_DB.id,Catalog_Server_DB.title).filter_by(topic=topic.replace("%20"," ")).all()
    if len(book)!=0:
        result = json.dumps(book,indent=2)
        return (result)
    else: 
        return jsonify({topic: "this topic does not exist "})

#2info 
@app.route("/info/<bookID>", methods=['GET'])
def get_info_forID(bookID):
    book = Catalog_Server_DB.query.with_entities(Catalog_Server_DB.title,Catalog_Server_DB.topic,Catalog_Server_DB.quantity,Catalog_Server_DB.price).filter_by(id = bookID).first()
    if book!= NullSession:
        result = json.dumps(book,indent=5)
        return (result)
    else: 
        return jsonify({bookID: "please try another id this not exist"})

#3:update price by admin
@app.route("/update_price/<bookID>",methods=['PUT'])
def update_book_price(bookID):
    getbook = Catalog_Server_DB.query.get(bookID)
    if getbook:
         #get price
        price = request.form.get('price')
        getbook.price = price 
        #save the update in DB
        db.session.commit() 
        book={}
        book['id']=getbook.id
        book['title']=getbook.title
        book['topic']=getbook.topic
        book['price']=getbook.price
        book['quantity']=getbook.quantity
        result = json.dumps(book,indent=5)
        return (result)
    else:
        return jsonify({bookID: "please try another id this not exist"})

#update quantity(increase quantity)
@app.route("/increase_quantity/<bookID>",methods=['PUT'])
def increase_book_quantity(bookID):
    getbook = Catalog_Server_DB.query.get(bookID)
    if getbook:
        new_amount = int(request.form.get('new_amount'))
        getbook.quantity = getbook.quantity + new_amount 
        db.session.commit()
        return jsonify({"msg" : f"increase number of book '{getbook.title}' done ! old quantity is {getbook.quantity-new_amount}, new quantity  {getbook.quantity}"})
    else:
        return jsonify({bookID: "please try another id this not exist"})

#decrease quantity
@app.route("/decrease_quantity/<bookID>",methods=['PUT'])
def decrease_book_quantity(bookID):
    getbook = Catalog_Server_DB.query.get(bookID)
    if getbook:
        new_amount = int(request.form.get('new_amount'))
        x= getbook.quantity - new_amount 
        if x < 0:
            return jsonify({"msg":f"no books enough ,the number of remaining books is {getbook.quantity}"})
        else :
            getbook.quantity = x
            db.session.commit()
        return jsonify({"msg" : f"decrease number of book : '{getbook.title}' done ! old quantity is {getbook.quantity+new_amount},  new quantity  {getbook.quantity}"})
    else:  return jsonify({bookID : "please try another id this not exist"})

if __name__ == '___main__':
    app.run(debug=True)
