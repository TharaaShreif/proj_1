from flask import Flask, Request, json, jsonify ,render_template, request_finished
from flask import request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


#(search operation )request to catalogServer
@app.route('/search/<topic>', methods=['GET'])
def search(topic): 
  re = request.get("http://172.16.224.195:5000/search/"+str(topic)) 
  return (re.content)



#(info operation )send request to the cataloge server 
@app.route('/info/<int:bookID>', methods=['GET'])
def get_info(bookID):
  #this is the request to be sent to the catalog server //tharaa pc
  re = request.get("http://172.16.224.195:5000/info/"+str(bookID))
  return (re.content)

#update the price of a book 

@app.route('/update_price/<int:bookID>', methods=['PUT'])
def update_book_price(bookID):
  price = request.json['price']
  #tharaa vm
  re = request.put("http://172.16.224.190:5000/update_price/"+str(bookID),data={'price':price})
  return (re.content)
#update quantity
#1increease
@app.route('/increase_quantity/<int:bookID>', methods=['PUT'])
def increase_book_quantity(bookID):
      
  new_amount = request.json['new_amount']
   #tharaa pc
  re = request.put("http://172.16.224.195:5000/increase_quantity/"+str(bookID),data={'new_amount':new_amount})
  return (re.content)
#2decreease
 
@app.route('/decrease_quantity/<int:bookID>', methods=['PUT'])
def decrease_book_quantity(bookID):
  new_amount = request.json['new_amount']
  re = Request.put("http://172.16.224.195.54:5000/decrease_quantity/"+str(bookID),data={'new_amount':new_amount})
  return (re.content)

#purchase (Order server requests)
@app.route('/purchase/<int:bookID>', methods=['PUT'])
def purchase(bookID):
    #tharaa vm
  r = request.put("http://172.16.224.195:5000/purchase/"+str(bookID)) 
  return (r.content)


if __name__=="__main__":
    app.run(debug=True)