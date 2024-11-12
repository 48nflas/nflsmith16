from pymongo import MongoClient
import certifi
import csv
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import dns.resolver
import numpy as np
#dns.resolver.default_resolver = dns.resolver.Resolver(configure=True)
#dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Atau gunakan ['1.1.1.1', '1.0.0.1'] untuk Cloudflare


#1. Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://dataanalyst:OtDwJ2z1KVkLJqeP@cluster0-ndqn7.mongodb.net/?ssl=true"
#2. Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

#BEGITULAH CARANYA MENGAKSES DATA DI DATABASE MELALUI VSC
#3. define collections
user = client.prod.users
truck = client.prod.trucks
order = client.prod.orders

seven_days_ago=datetime.now()-timedelta(days=7)
x=datetime(2024,1,1,0,0,0,0)
y=datetime(2024,2,1,0,0,0,0)
recent_order=order.find({
    "createdAt": {"$gte": seven_days_ago}
})  

z = datetime(2024,1,1,0,0,0,0)+3*timedelta(days=3)
print(datetime.now())
active_drivers=user.find({
    "$and":[
        {"role":"driver"},
        {"updatedAt":{"$gte":seven_days_ago}}
    ]
})

active_users = user.find({"updatedAt":{"gte":seven_days_ago}})


active_trucks=truck.find({"updatedAt":{"gte":seven_days_ago}})

last_7_days_orders=order.find({"createdAt":{"gte":seven_days_ago}})
#print(seven_days_ago) 
q1={"createdAt":{"$gte":x}}
q2={"createdAt":{"$lt":y}}
q3={"createdAt":{"$lt":z}}
print(order.count_documents({}))
order_jan_2024=order.find({"$and":[q1,q2]})
print(order.count_documents({"$and":[q1,q2]}))
print(order_jan_2024)
data1=order.find({"$and":[q1,q3]}).limit(2)
data2=order.find({"createdAt":{"$gte":datetime(2024,9,1,0,0,0,0)}}).limit(1)
for x in data2:
    print(x)
#for x in data1:
#    print(x)
#for x in data1:
#    print(x)

l1=[]
for i in range(1,32):
    l1.append(order.count_documents({"$and":[{"createdAt":{"$gte":datetime(2024,1,i,0,0,0,0)}},{
        "createdAt":{"$lt":(datetime(2024,1,i,0,0,0,0)+timedelta(days=1))}
    }]}))
#print(l1)

l2=[]
for i in range(1,30):
    l2.append(order.count_documents({"$and":[{"createdAt":{"$gte":datetime(2024,2,i,0,0,0,0)}},{
        "createdAt":{"$lt":(datetime(2024,2,i,0,0,0,0)+timedelta(days=1))}
    }]}))
#print(l2)

l3=[]
for i in range(1,32):
    l3.append(order.count_documents({"$and":[{"createdAt":{"$gte":datetime(2024,3,i,0,0,0,0)}},{
        "createdAt":{"$lt":(datetime(2024,3,i,0,0,0,0)+timedelta(days=1))}
    }]}))
#print(l3)

def data(x):
    l=['Data',[1,31,'Januari'],[2,(29 if x%4==0 else 28),'Februari'],[3,31,'Maret'],[4,30,'April'],[5,31,'Mei'],
       [6,30,'Juni'],[7,31,'Juli'],[8,31,'Agustus'],[9,30,'September'],[10,31,'Oktober'],
       [11,30,'November'],[12,31,'Desember']]
    return l

def heatmap_visualization(year,month):
    li=[]
    for _ in range(1,data(year)[month][1]+1): ##
        li.append([])
    for j in range(1,data(year)[month][1]+1): ##
        for i in range(24):
            li[j-1].append(order.count_documents({"$and":[{"createdAt":{"$gte":datetime(year,month,j,i,0,0,0)}},{
        "createdAt":{"$lt":(datetime(year,month,j,i,0,0,0)+timedelta(hours=1))}
    }]}))
    #print(li)


    l=[]
    for x in range(24):
        l.append(str('{}-{}'.format(str(x),str(x+1))))
    #print(l)
    #print(np.array(l))
    y=[]
    for x in range(1,data(year)[month][1]+1): ##
        y.append(x)
    #18 tahapan
    plt.figure(figsize=(100, 50))  # Ukuran heatmap
    sns.heatmap(li, annot=True, cmap="Reds",yticklabels=y,xticklabels=l)  # `annot=True` menampilkan nilai tiap sel
    plt.title("Heatmap banyaknya order yang dibuat (permintaan pengiriman barang) bulan {} {}".format(data(year)[month][2],str(year)))
    plt.xlabel("Jam")
    plt.ylabel("Tanggal")
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9.5)
    plt.show()


for y in range(2024,2025):
    for mo in range(1,11):
        heatmap_visualization(y,mo)
