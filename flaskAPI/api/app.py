
# This is a basic forwarding component used in the article:
# Authors: Nam-Thang Hoang, Hai-Anh Tran, Cong-Son Duong, Tran-Le-Tuan Nguyen
# SOICT 

# In this program, there are 2 components: 
# Component 1: API to receive data from SINA system in the article: https://doi.org/10.3390/electronics11070975 
# data will be calculated by us QoS parameters save to local database
# Component 2: We implement apis to communicate with other SDNs with mechanism Adaptive Consistency and with CCDN

import logging
import sys

PATH_ABSOLUTE = "/home/onos/Downloads/flask_SDN/Flask-SDN/"
sys.path.append(PATH_ABSOLUTE+'flaskAPI/dataBaseMongo')
sys.path.append(PATH_ABSOLUTE+'flaskAPI/linkTopo')

from flask import Flask, request, jsonify

# import database
import LinkVersion, learnWeight, lstmWeight, EndPoint
import updateWeight, LearnWeightModel, LinkVersion
import pub
import time
import json
import requests

# ignore log in flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Init app
app = Flask(__name__)

ip_ccdn = str(json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['ip_ccdn'])
update = updateWeight.updateWeight()

_learnWeight = learnWeight.learnWeight()

# set start time of program
starttime = time.time()

# communicate with ryu controller
@app.route('/write_data_ryu/',  methods=['GET', 'POST'])
def write_data_ryu():
    content = request.data
    data = json.loads(content)
    if float(data['byteSent']) > 600 and float(data['byteReceived']) > 600:
        # Params.insert_n_data(data)
        pub.connectRabbitMQ(data=data)
    return 'Sondzai'


# communicate with onos controller
@app.route('/write_data/',  methods=['GET', 'POST'])
def write_data():
    global starttime
    if request.method == 'GET':
        return "Da nhan duoc GET"

    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data.decode("utf-8") 
        dicdata = {}
        datas = content.split("&")
        # processing data
        for data in datas:
            d = data.split(":")
            if len(d) == 3:
                temp = [d[1], d[2]]
                dicdata[d[0]] = ":".join(temp)
            else:
                dicdata[d[0]] = d[1]
  
        #  remove default data
        dicdata['byteReceived'] = float(dicdata['byteReceived']) * 10**-6 # Byte => MB
        dicdata['byteSent'] = float(dicdata['byteSent']) * 10**-6         # Byte => MB
        check_overhead = ( float(dicdata['byteReceived']) + float(dicdata['byteSent']) ) / 2  
        dicdata['overhead'] = check_overhead
        threshold_min = 0.8
        threshold_max = 70

        # loai bo du lieu ao
        if threshold_min < check_overhead < threshold_max:
            print("****************** Cap nhat du lieu ******************")
            update.update_link_params(dicdata)

        # print("LinkVersionN TAI: ", time.time() - starttime )
        if time.time() - starttime > 45:
            print("GUI DATA CHO CCDN")
            data_temp = LinkVersion.get_multiple_data()
            # chia TB cac tham so
            for d in data_temp:
                d_tmp = {
                        'src': d['src'],
                        'dst': d['dst'],
                        'delay': float(d['delay'])/float(d['count']),
                        'linkUtilization': float(d['linkUtilization'])/float(d['count']),
                        'packetLoss': float(d['packetLoss'])/float(d['count']),
                        'overhead': float(d['overhead'])/float(d['count']),
                        'byteSent': float(d['byteSent'])/float(d['count']),
                        'byteReceived': float(d['byteReceived'])/float(d['count'])
                    }
                url_ccdn = "http://" + ip_ccdn + ":5000/write_full_data/"
                requests.post(url_ccdn, data=json.dumps({'link_versions': d_tmp}))

            LinkVersion.remove_all()
            starttime = time.time()

        return content

#SERVER COST FROM ONOS 
@app.route('/write_server_data/',  methods=['GET', 'POST'])
def write_server_data():
    if request.method == 'GET':
        return "Da nhan duoc GET"

    if request.method == 'POST':
        # app.logger.info("Da nhan dc POST")
        content = request.data.decode("utf-8") 
        dicdata = {}
        datas = content.split("&")
        # processing data
        for data in datas:
            # print(data)
            d = data.split(":")
            if len(d) == 3:
                temp = [d[1], d[2]]
                dicdata[d[0]] = ":".join(temp)
            else:
                dicdata[d[0]] = d[1]

        # print(dicdata)
        data_search = {'srcLink': dicdata['srcLink'], 'portInfo': dicdata['portInfo']}
        if EndPoint.is_data_exit(data_search=data_search):
            EndPoint.update_many(data_search, dicdata)
        else:
            EndPoint.insert_data(data=dicdata)
        
        # # write to CCDN
        url_ccdn = "http://" + ip_ccdn + ":5000/write_EndPoint/"
        requests.post(url_ccdn, data=json.dumps({'EndPoint_datas': dicdata}))
        return content

def write_learn_weights_ccdn():
    # Get data from local and upload to ccdn database
    data = LearnWeightModel.get_multiple_data()
    url_ccdn = "http://" + ip_ccdn + ":5000/write_learn_weights/"
    requests.post(url_ccdn, data=json.dumps({ data}))
    return 

# @app.route('/write_W_SDN/',  methods=['GET', 'POST'])
# def write_W_SDN():
#     # API: Get N_w parameter from CCDN and write to local data of N_w SDNs
#     if request.method == 'POST':
#         W_contant = request.data
#         update.write_W_SDN(int(W_contant))
#         return W_contant


@app.route('/write_link_version/',  methods=['GET', 'POST'])
def write_link_version():
    # API: receive data from other SDNs sent to
    if request.method == 'POST':
        content = request.data
        for data in json.loads(content)['link_versions']:
            data_search = { 'src': data['src'], 'dst': data['dst'] }
            if LinkVersion.is_data_exit(data_search=data_search):
                LinkVersion.update_many(data_search, data)
            else:
                LinkVersion.insert_data(data=data)
        return content

@app.route('/read_link_version/',  methods=['GET', 'POST'])
def read_link_version():
    # API: get data from load send to CCDN when there is a request to read N_r SDNs
    if request.method == 'GET':
        data = LinkVersion.get_multiple_data()
        return jsonify({'link_versions': data})  # will return the json

@app.route('/write_W_SDN/',  methods=['GET', 'POST'])
def write_W_SDN():
    # API: Get N_w parameter from CCDN and write to local data of N_w SDNs
    if request.method == 'POST':
        W_contant = request.data
        learnWeight.write_W_SDN(int(W_contant))
        return W_contant

@app.route('/write_learn_link/',  methods=['GET', 'POST'])
def write_learn_link():
    # API: receive data from other SDNs sent to
    if request.method == 'POST':
        content = request.data
        for data in json.loads(content)['learn_link']:
            data_search = { 'src': data['src'], 'dst': data['dst'] }
            if LearnWeightModel.is_data_exit(data_search=data_search):
                LearnWeightModel.update_many(data_search, data)
            else:
                LearnWeightModel.insert_data(data=data)
        return content

@app.route('/read_learn_link/',  methods=['GET', 'POST'])
def read_learn_link():
    # API: get data from load send to CCDN when there is a request to read N_r SDNs
    if request.method == 'GET':
        data = LearnWeightModel.get_multiple_data()
        return jsonify({'learn_link': data})  # will return the json


if __name__ == '__main__':
    ip_local = str(json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['ip_local'])
    app.run(host=ip_local, debug=True, use_reloader=False)
