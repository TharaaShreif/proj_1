from flask import Flask, json
from flask import request
from flask import jsonify

from flask.sessions import NullSession

from flask_marshmallow import Marshmallow
from marshmallow.fields import Integer
from marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BooksInfo_DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Catalog_DB(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(600))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    topic = db.Column(db.String(600))
     

    def __init__(self,id,title,quantity,price,topic):
        self.id=id
        self.title=title
        self.quantity=quantity
        self.price=price
        self.topic=topic
        
book={}


#1:search,get all books that have spicific topic
@app.route("/search/<topic>", methods=['GET'])
def search_by_topic(topic):
    book = Catalog_DB.query.with_entities(Catalog_DB.id,Catalog_DB.title).filter_by(topic=topic.replace("%20"," ")).all()
    if len(book)!=0:
        re = json.dumps(book,indent=2)
       
        return (re)
    else: 
        return jsonify({topic: "this topic does not exist "})

#2:info,get the information of book  that have spicific id
@app.route("/info/<bookID>", methods=['GET'])
def get_info_forID(bookID):
    book = Catalog_DB.query.with_entities(Catalog_DB.title,Catalog_DB.topic,Catalog_DB.quantity,Catalog_DB.price).filter_by(id = bookID).first()
    if book!= NullSession:
        re = json.dumps(book,indent=5)
        return (re)
    else: 
        return jsonify({bookID: "please try another id this not exist"})

#3:update price by admin
@app.route("/update_price/<bookID>",methods=['PUT'])
def update_book_price(bookID):
    getbook = Catalog_DB.query.get(bookID)
    if getbook:
         #get price
        price = request.form.get('price')
        getbook.price = price 
 
        db.session.commit()        #save the update in DB
        book={}
        book['id']=getbook.id
        book['title']=getbook.title
        book['topic']=getbook.topic
        book['price']=getbook.price
        book['quantity']=getbook.quantity
        re = json.dumps(book,indent=5)
        return (re)
    else:
        return jsonify({bookID: "please try another id this not exist"})

#update quantity(increase quantity)
@app.route("/increase_quantity/<bookID>",methods=['PUT'])
def increase_book_quantity(bookID):
    getbook = Catalog_DB.query.get(bookID)
    if getbook:
        new_amount = int(request.form.get('new_amount'))
        getbook.quantity = getbook.quantity + new_amount 
        db.session.commit()
        return jsonify({"message" : f"increase # of book '{getbook.title}' done !!  new quantity  {getbook.quantity}"})
    else:
        return jsonify({bookID: "please try another id this not exist"})

#decrease quantity
@app.route("/decrease_quantity/<bookID>",methods=['PUT'])
def decrease_book_quantity(bookID):
    getbook = Catalog_DB.query.get(bookID)
    if getbook:
        new_amount = int(request.form.get('new_amount'))
        x= getbook.quantity - new_amount 
        if x < 0:
            return jsonify({"message":f"no book enough ,#of remaining books is {getbook.quantity}"})
        else :
            getbook.quantity = x
            db.session.commit()
        return jsonify({"message" : f"decrease # of book : '{getbook.title}' done !! new quantity  {getbook.quantity}"})
    else:  return jsonify({bookID : "please try another id this not exist"})

if __name__ == '___main__':
    app.run(debug=True)
