import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
import Server_Info, Server_Info_Full
import json
import time
import sys

import ast

def find_sub_string(start, end, text):
    start_index, end_index = 0, 0
    try:
        start_index = text.index(start)
        end_index = text.index(end)
    except:
        print("Tim chuoi that bai")

    return text[start_index: end_index + 1]
      
   

text = "{'ping': '4', 'upload': 880.13472, 'download': 1650.91893, 'respone_time': 3, 'server_ip': '10.0.0.3'}"
start = "{"
end = "}"
data = ast.literal_eval(find_sub_string(start, end, text) )
Server_Info_Full.insert_data(data)
if Server_Info.is_data_exit(data['server_ip']):
    Server_Info.update_many(data['server_ip'], data)
else:
    Server_Info.insert_data(data)