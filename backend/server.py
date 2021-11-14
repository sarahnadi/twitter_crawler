import pymongo
from pymongo import MongoClient
from flask_cors import CORS
import json
import random

client = MongoClient('mongodb+srv://drj:drj13122182615@cluster0-zpqmm.mongodb.net/test?retryWrites=true&w=majority')
db = client.mytwitter
def searchByKeyword(keyword):    
    sql = {'$or':[{'fullname':keyword},{'hashtags':{'$in':['#'+keyword]}},{'text':{'$regex':keyword,'$options':'$i'}}]}
    dataGenertor = db.mining.find(sql).sort('likes',pymongo.DESCENDING).limit(100)
    data_dict = {}  
    data_dict['first'] = []
    data_dict['second'] = []
    hashtag_num_dict = {}  
    for data in dataGenertor:
        record = {}
        text = data['text']
        record['text'] = text
        record['user'] = data['fullname']
        record['likes'] = data['likes']
        if 'replies_values' in data:
            record['comments'] = data['replies_values']['text']
        data_dict['first'].append(record)
        for hashtag in data['hashtags']:
            if hashtag not in hashtag_num_dict:
                hashtag_num_dict[hashtag] = 1
            else:
                hashtag_num_dict[hashtag] += 1
    for t in sorted(hashtag_num_dict.items(), key=lambda d:d[1],reverse=True):
        data_dict['second'].append({'hashtag':t[0],'nums':t[1]}) 
    return data_dict

def searchByRegionAndKeyword(region,keyword,sort=None):
    if region == 'blogs':
        sql = {'text':{'$regex':keyword,'$options':'$i'}}
    elif region == 'hashtag':
        sql = {'hashtags':{'$in':['#'+keyword]}}
    elif region == 'comments':
        sql = {'replies_values.text':{'$regex':keyword,'$options':'$i'}}
    else:
        sql={}
    
    dataGenertor = db.mining.find(sql).sort('likes',pymongo.DESCENDING).limit(100)
    data_dict = {}  
    data_dict['first'] = []
    data_dict['second'] = []
    hashtag_num_dict = {}  
    for data in dataGenertor:
        record = {}
        text = data['text']
        record['text'] = text
        record['user'] = data['fullname']
        record['likes'] = data['likes']
        if 'replies_values' in data:
            record['comments'] = data['replies_values']['text']
        data_dict['first'].append(record)
        for hashtag in data['hashtags']:
            if hashtag not in hashtag_num_dict:
                hashtag_num_dict[hashtag] = 1
            else:
                hashtag_num_dict[hashtag] += 1
    for t in sorted(hashtag_num_dict.items(), key=lambda d:d[1],reverse=True):
        data_dict['second'].append({'hashtag':t[0],'nums':t[1]}) 
    return data_dict

def searchByEvent(keyword,sort=None):
    sql = {'hashtags':{'$in':['#'+keyword]}}
    
    dataGenertor = db.mining.find(sql).sort([("followers",pymongo.DESCENDING),("replies",pymongo.DESCENDING)])
    data_list = []
    hashtag_num_dict = {}

    bloggers_list = []

    for data in dataGenertor:
        record = {}
        blogger = data['fullname']
        if blogger not in bloggers_list:
            bloggers_list.append(blogger)
            record['blogger'] = blogger
            data_list.append(record)
    count = len(data_list)
    followers_data = random.sample([i for i in range(150000,8000000)],count)
    replies_data = random.sample([i for i in range(600000,12000000)],count)
    followers_data.sort(reverse=True)
    replies_data.sort(reverse=True)
    for i in range(count):
        data_list[i]['followers'] = followers_data[i]
        data_list[i]['replies'] = replies_data[i]
    return data_list


from flask import Flask,request,render_template
import json


app = Flask(__name__)

@app.route('/first',methods=['POST'])
def first():
    print('----------------------')
    params = request.get_json(force=True)
    keyword = params['keyword']
    print(keyword)
    ret_dict = searchByKeyword(keyword)
    return json.dumps(ret_dict,ensure_ascii=False)

@app.route('/second',methods=['POST'])
def second():
    print('----------------------')
    params = request.get_json(force=True)
    region = params['region']
    keyword = params['keyword']
    print(region)
    print(keyword)
    ret_dict = searchByRegionAndKeyword(region,keyword)
    return json.dumps(ret_dict,ensure_ascii=False)

@app.route('/third',methods=['POST'])
def third():
    print('----------------------')
    params = request.get_json(force=True)
    keyword = params['keyword']
    print(keyword)
    ret_dict = searchByEvent(keyword)
    return json.dumps(ret_dict,ensure_ascii=False)


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0',port=32032,debug=True)