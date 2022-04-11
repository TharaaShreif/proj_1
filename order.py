from flask import Flask, json, jsonify ,render_template
from flask import request
from flask_sqlalchemy.model import Model
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
from datetime import datetime
import sqlite3



#initial app
app = Flask(__name__)


#purchase 
# if client send purchase with a specific book_id then order server send to catalog server

@app.route('/purchase/<int:bookID>', methods=['PUT'])
def purchase_book(bookID):
    re=request.put("http://172.16.224.195:5000/decrease_quantity/"+str(bookID),{'new_amount':16})
    x=re.json()
    message= str(x.get('message'))
    

    if message.find("enough")!=-1:
      
        return(re.content)
    else: 
        
        re2=request.get("http://172.16.224.195:5000/info/"+str(bookID))
        info=re2.json()
        return {"message":f"bought book '{info.get('title')}'"}
      


#run the prog
if __name__=="__main__":
    app.run(debug=True)
