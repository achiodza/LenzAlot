import os
import datetime
from magic import CamInt
import pymongo
from flask import Flask, flash, render_template, request, redirect, url_for
from bson import json_util, abc
import json
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'unityushe@gmail.com'
app.config['MAIL_PASSWORD']='67babez!'

mail=Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    #list_re = value.split()
    #print(type(list_re))
    #test = (list_re[3])
    date = datetime.datetime.now()
  

    return render_template('app.html',  date=date)


@app.route('/start/camera', methods=['GET', 'POST'])
def startCam():

  
    #motion=magic.CamInt()
    date = datetime.datetime.now()
    CamInt()


    return render_template('app.html',  date=date)


@app.route('/results', methods=['GET', 'POST'])
def results():


    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lenz"]
    mycol = mydb["mafirimu"]

    x = mycol.aggregate([{'$sort': {'_id': -1}}, {'$limit': 5}])
    json_results = []
    for result in x:
        json_results.append(result)
    return json.dumps(json_results, default=json_util.default)


@app.route('/email/sent')
def process():
    
    subject="Report "
    body= results()
    msg=Message(body=body, subject=subject, sender='unityushe@gmail.com', recipients=['h150312p@hit.ac.zw'])
    mail.send(msg)
    date = datetime.datetime.now()
    

    

    return render_template('app.html', date=date)


if __name__ == '__main__':
    app.run(debug=True)
