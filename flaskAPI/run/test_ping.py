import requests

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://10.20.0.201:5000/getIpServer", data= host)  
    dest_ip = response.text
    return str(dest_ip)


des = call_routing_api_flask( '10.0.0.1' )
# des = "10.0.0.4"
print("TRUYEN DU LIEU ", '10.0.0.1', "--->", des)