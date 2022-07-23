import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/dataBaseMongo')
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/api')


import LinkVersion

datas_link = LinkVersion.find_data_link( "of:0000000000000002", "of:0000000000000001",)
print(datas_link)