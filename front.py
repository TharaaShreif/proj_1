from flask import Flask, Request, json, jsonify ,render_template, request_finished
from flask import request
from flask_sqlalchemy import SQLAlchemy


#initial app
app = Flask(__name__)
#search operation 
#getting the books info request to catalogServer
@app.route('/search/<topic>', methods=['GET'])
def search(topic): 
  result = request.get("http://172.16.224.54:5000/search/"+str(topic)) #send request to catalog server
  return (result.content)


#============================== 2- info operation ====================================
#send request to the cataloge server to get information about id book
@app.route('/info/<int:bookID>', methods=['GET'])
def get_info(bookID):
  #this is the request to be sent to the catalog server //tharaa pc
  result = request.get("http://172.16.224.54:5000/info/"+str(bookID))
  return (result.content)

#============================= 3- update price ========================================

#update the price of a book 
@app.route('/update_price/<int:bookID>', methods=['PUT'])
def update_book_price(bookID):
  price = request.json['price']
  #tharaa vm
  result = request.put("http://172.19.224.20:5000/update_price/"+str(bookID),data={'price':price})
  return (result.content)

#============================= 4- update quantity ========================================

            #=================== increease quantity =================
 
@app.route('/increase_quantity/<int:bookID>', methods=['PUT'])
def increase_book_quantity(bookID):
  new_amount = request.json['new_amount']
   #tharaa pc
  result = request.put("http://172.19.224.54:5000/increase_quantity/"+str(bookID),data={'new_amount':new_amount})
  return (result.content)

            #=================== decreease quantity =================
 
@app.route('/decrease_quantity/<int:bookID>', methods=['PUT'])
def decrease_book_quantity(bookID):
  new_amount = request.json['new_amount']
  result = Request.put("http://172.19.224.54:5000/decrease_quantity/"+str(bookID),data={'new_amount':new_amount})
  return (result.content)


#==============================================================================================
#============================ Order server requests ===========================================
#==============================================================================================

#====================== purchase ====================================================
@app.route('/purchase/<int:bookID>', methods=['PUT'])
def purchase(bookID):
    #tharaa vm
  r = request.put("http://172.19.224.20:5000/purchase/"+str(bookID)) 
  return (r.content)


if __name__=="__main__":
    app.run(debug=True)