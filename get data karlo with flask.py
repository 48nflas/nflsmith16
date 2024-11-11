from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
import certifi
import csv
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import dns.resolver
import numpy as np

app= Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dataanalyst:OtDwJ2z1KVkLJqeP@cluster0-ndqn7.mongodb.net/?ssl=true"
mongo=PyMongo(app)

user=mongo.prod.users
truck=mongo.prod.trucks
order=mongo.prod.orders
skrg=datetime.now()

#format : app.route - route string, methodnya apa
@app.route('/activedrivers',methods=['GET'])
def get_active_drivers(d):
    active_driver_data=user.find({
    "$and":[
        {"role":"driver"},
        {"updatedAt":{"$gte":skrg-timedelta(days=d)}}
    ]
})
    return {"success":True,"data":active_driver_data}

@app.route('/activetrucks',methods=['GET'])
def get_active_trucks(d):
    return {"success":True,"data":truck.find({"updatedAt":{"gte":skrg-timedelta(days=d)}})}

@app.route('/orders',methods=['GET'])
def get_orders(y1,m1,d1,h1,min1,sec1,ms1,y2,m2,d2,h2,min2,sec2,ms2):
    order_data=order.find({"$and":[{"createdAt":{"$gte":datetime(y1,m1,d1,h1,min1,sec1,ms1)}},{
        "createdAt":{"$lte":(datetime(y2,m2,d2,h2,min2,sec2,ms2))}
    }]})
    return {"success":True,"data":order_data}

@app.route('/activeusers',methods=['GET'])
def get_active_users(d):
    active_users_data= user.find({"updatedAt":{"gte":skrg-timedelta(days=d)}})
    return {"success":True,"data":active_users_data}

if __name__=='__main__':
    app.run()