
import sys,os
PATH_ABSOLUTE = str(os.environ.get('PATH_ABSOLUTE'))
sys.path.append(PATH_ABSOLUTE+'handledata/models')
sys.path.append(PATH_ABSOLUTE+'core')

import flowRule
import Dijkstra

class hostServerConnectionRR(object):

    def __init__(self, topo_network, hosts, servers, index_server, priority):
        """
        topo: object topo network
        hosts: dictionary of host (key: ip, value: object)
        servers: dictionary of server (key: ip, value: object)
        """
        self.topo = topo_network
        self.hosts = hosts
        self.servers = servers
        self.index_server = index_server
        self.priority = priority

        # cap nhap lai trong so cua mang khi co thay doi
        # self.update_topo()

        # khoi tao thuat toan tim duong
        self.sol = ""
        self.reverse_sol = ""
        
        # add flow
        self.flow = ""
        self.reverse_flow = ""

        # host and des ip
        self.host_ip = ""
        self.dest_ip = ""

    def set_host_ip(self, host_ip):
        self.host_ip = host_ip

    def update_topo(self, link_versions):
        self.topo.read_update_weight(link_versions)
    
    def find_src(self):
        try:
            host_object = self.hosts[self.host_ip]     
        except:
            print("Khong ton tai ip", self.host_ip)
        return host_object

    def find_shortest_path(self):
        
        # get host object
        host_object = self.find_src()

        # Co che quay vong doi tuong cua Round robin
        # self.queue_rr.receive_queue()
        dest_ip = list(self.servers)[self.index_server]
        # self.queue_rr.connectRabbitMQ(ip_dest= dest_ip)

        # get dest objkect    
        dest_object = self.servers[dest_ip]


        print("INDEX: ", self.index_server)
        print("SERVER: ", dest_object.get_id())
        
        # khoi tao tap duong di de add flow
        path = ""

        # di chieu xuoi 
        self.sol = Dijkstra.Dijkstra( topo=self.topo, start= host_object, end= dest_object)
        self.sol.routing()

        # print("cost server=", dest_object.get_server_cost())
        # self.write_server_cost(dest_object, dest_ip)

        # lay path tu diem dau den diem cuoi va add flow vao path
        path = self.sol.get_result()
        self.add_flow(host_object, dest_object, path)
      
        return dest_ip 
      
    def write_server_cost(self, dest_object, dest_ip):
        url = "/home/onos/Downloads/flaskSDN/serverCost.txt"
        with open(url, "a") as file_object:
            data = "server " + str(dest_ip ) + "       =" + str( dest_object.get_server_cost() ) + "\n"
            file_object.write(data)
            file_object.write("++++++++++++++++++++++++++++++++++++++++++++") 

    def add_flow(self, host_object, dest_object, path):

        # di chieu nguoc
        self.reverse_sol = Dijkstra.Dijkstra( topo=self.topo, start= dest_object, end= host_object)
        self.reverse_sol.routing()
        reverse_path = self.reverse_sol.get_result()

        # add flow chieu thuan    
        # print("\n\nadd flow JSon")
        flow = flowRule.flowRule(topo = self.topo, shortest_path = path, src = host_object, dst = dest_object)
        flow.add_flow_rule(self.priority)
        flow_rule = flow.get_json_rule()

        # add flow chieu nguoc
        # print("\n\nadd reverse flow JSon")
        reverse_flow = flowRule.flowRule(topo = self.topo, shortest_path = reverse_path, src = dest_object, dst = host_object)
        reverse_flow.add_flow_rule(self.priority)
        reverse_flow_rule = reverse_flow.get_json_rule()
        
        flow.write_json_rule_to_file(json_rule_path = flow_rule, 
                                 json_rule_reversing_path= reverse_flow_rule)

    
