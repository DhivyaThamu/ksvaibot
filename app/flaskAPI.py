
from flask.templating import render_template
import requests
from flask import Flask,request,jsonify
import adodbapi
from flask_cors import CORS
import pyodbc

#conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      #'Server=ksvconnectivr.cv1q1qoubsbl.us-east-1.rds.amazonaws.com;'
                      #'Database=Test;'
                      #'UID=admin;'
                      #'PWD=Muruga275;'
                      #'Trusted_Connection=yes;')

app=Flask(__name__)
CORS(app)
app.config['Debug']=True
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def form():
    return render_template('index.html')

#@app.route('/chat',methods=['Get','Post'])
@app.route('/',methods=['POST'])
def rasa():

    #if request.method == 'POST':
        #id = request.get_json()['id']
        #msg = request.get_json()['msg']

    id = request.form['id']
    msg = request.form['msg']

    url = 'http://localhost:5005/webhooks/rest/webhook'

    data = {'sender':id,'message':msg}

    #cursor=conn.cursor()
    #cursor.execute('INSER INTO TEST_TABLE (EMP_NAME) VALUES ('+msg+')')

    result = requests.post(url = url,json = data)


    return jsonify(result.json())
    
        
if __name__=="__main__":
    app.run()

