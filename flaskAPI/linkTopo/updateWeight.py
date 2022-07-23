import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/dataBaseMongo')
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/api')

import json, time
import requests
import random
import LinkVersion
import sub
import linkWeight
import LinkVersion

class updateWeight(object):

    def __init__(self):
        self.params_data = ""
        self.link_set = list()
        self.consumer = sub.Sub()
        self.link_version = 0
        self.save_linkVersion = dict()

        # So lan write ra nhieu SDN
        self.ip_local = str(json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['ip_local'])
        self.ip_remote = json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['ip_remote']
        self.ip_ccdn =  str(json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['ip_ccdn'])
        self.thread_overhead =  float(json.load(open('/home/onos/Downloads/flask_SDN/config.json'))['thread_overhead'])
        self.count = 0
        # self.ip_sdn = ['10.20.0.251']

    def get_link_set(self):
        return self.link_set

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def reset_link_set(self):
        self.link_set = list()

    def read_params_from_rabbit(self):
        # pop data from RAbbit Queue
        self.consumer.receive_queue()
        # self.params_data = self.consumer.peek_stack()
        self.params_data = self.consumer.pop_stack()


        self.update_link()

    def update_link_params(self, dicdata):
        """
        Cong don cac link trung nhau va lay trung binh
        
        """
        # update QoS from SINA data and insert into batabase (dataset)
        src = dicdata['src']
        dst = dicdata['dst']
        delay = float(dicdata['delay'])
        # linkUtilization = float(dicdata['linkUtilization']) if float(dicdata['linkUtilization']) == 1.0 else random.uniform(0, 0.7)
        linkUtilization = float(dicdata['linkUtilization'])
        packetLoss = float(dicdata['packetLossRate'])
        byteSent = float(dicdata['byteSent']) 
        byteReceived = float(dicdata['byteReceived'])
        # overhead = (byteSent + byteReceived) / 1000000 # convert to MB
        overhead = float(dicdata['overhead'])  # convert byte/s => Mb/s
        
        tmp_name = src + dst
        if self.save_linkVersion.get(tmp_name) is None:
            self.save_linkVersion[tmp_name] = 1

        temp_data = {"src": src,
                    "dst": dst,
                    "delay": float(delay),
                    "linkUtilization": float(linkUtilization),
                    "packetLoss": float(packetLoss),
                    "overhead": float(overhead),
                    "byteSent": float(byteSent),
                    "byteReceived": float(byteReceived),
                    "count": 1,
                    "linkVersion": 1
            }


        # try:
            #kiem tra xem link co ton tai chua
        data_search = {'src': temp_data['src'], 'dst': temp_data['dst']}
        if LinkVersion.is_data_exit(data_search=data_search):
                # neu ton tai thi cap nhap lai Qos link
                # print("cap nhap link ton tai")
                self.update_link_exit(src=src, dst=dst, temp_data=temp_data, data_search=data_search)
                # LinkVersion.update_many(data_search, new_data)
        else:
                # print("chen link moi")
                LinkVersion.insert_data(temp_data)
                # print("Ghi vao local may nay thanh cong")
        # except:
        #     print("--------------- Write LinkVersion loi")

    def update_link_exit(self, src, dst, temp_data, data_search):
        datas_link = LinkVersion.find_data_link(src, dst)
        # print(datas_link)


        data_link = datas_link[0]
        # print(data_link)

        # cong don data moi va data cu trong DB
        delay = temp_data['delay'] + data_link['delay']
        linkUtilization =  temp_data['linkUtilization'] + data_link['linkUtilization']
        packetLoss = temp_data['packetLoss'] + data_link['packetLoss']
        overhead = temp_data['overhead'] + data_link['overhead']
        byteSent = temp_data['byteSent'] + data_link['byteSent']
        byteReceived = temp_data['byteReceived'] + data_link['byteReceived']
        count = temp_data['count'] + data_link['count']
        temp_name = src + dst
        self.save_linkVersion[temp_name] = temp_data['linkVersion'] + self.save_linkVersion[temp_name]
        new_temp_data = {"src": src,
                        "dst": dst,
                        "delay": float(delay),
                        "linkUtilization": float(linkUtilization),
                        "packetLoss": float(packetLoss),
                        "overhead": float(overhead),
                        "byteSent": float(byteSent),
                        "byteReceived": float(byteReceived),
                        "count": count,
                        "linkVersion": self.save_linkVersion[temp_name]
            }

        # print(new_temp_data)
        # cap nhap lai QoS link
        print(new_temp_data)
        LinkVersion.update_many(data_search, new_temp_data)

    # def update_link(self):
    #     link = None 
    #     id_src = str(self.params_data['src'])
    #     id_dst = str(self.params_data['dst'])
    #     link = self.has_link(target_src=id_src, target_dst=id_dst)
    #     # print("khoi tao", id_src, "-->>", id_dst)
    #     # print("data = ", self.params_data)

    #     # Neu link chua co trong tap canh thi khoi tao link
    #     if link == None:
    #         # print("khoi tao", id_src, "-->>", id_dst)
    #         link_object = linkWeight.linkWeight(id_src=id_src, id_dst=id_dst)
    #         self.link_set.append(link_object)
    #         link_object.update_weight(params_data=self.params_data)
    #     # neu link da co trong tap canh thi cap nhat lai weight
    #     else:
    #         link.update_weight(params_data=self.params_data)

    # def has_link(self, target_src, target_dst):
    #     print("chay")
    #     print("can tim", target_src, target_dst)
    #     print("dang tim")
    #     print(self.link_set)
    #     for link in self.link_set:
    #         print(link.get_id_src(), link.get_id_dst())
    #         if str(link.get_id_src()) == target_src and str(link.get_id_dst()) == target_dst:
    #             print("ok")
    #             return link
    #     return None

    def write_update_link_to_data_base(self):
        # try:
        #     LinkVersion.remove_all()
        # except:
        #     print("Remove loi .................")

        self.link_version += 1
        self.count += 1

        # start_time = time.time()
        for link in self.link_set:
            src = link.get_id_src()
            dst = link.get_id_dst()
            # print("chay lan thu", self.count)
            weight = link.find_link_cost()

            delay = weight[0]
            link_utilization = weight[1]
            packet_loss = weight[2]
            byte_sent = weight[3]
            byte_received = weight[4]

            overhead = (byte_sent + byte_received) / 2

            if (overhead > 12):
                ratio_overhead = (overhead - 12)/12
            else:
                ratio_overhead = 0

            temp_data = {"src": src,
                        "dst": dst,
                        "delay": float(delay),
                        "linkUtilization": float(link_utilization),
                        "packetLoss": float(packet_loss),
                        "IpSDN": self.ip_local,
                        "overhead": float(overhead),
                        "ratio_overhead": float(ratio_overhead),
                        "byteSent": float(byte_sent),
                        "byteReceived": float(byte_received)
            }
            try:
                data_search = { 'src': temp_data['src'], 'dst': temp_data['dst'] }
                # print("INSERT LINK VERSION")
                if LinkVersion.is_data_exit(data_search=data_search):
                    LinkVersion.update_many(data_search, temp_data)
                else:
                    LinkVersion.insert_data(data=temp_data)
                # print("Ghi vao local may nay thanh cong")

                # ghi vao ccdn de thong ke
                self.write_ccdn(temp_data)
            except:
                print("--------------- Write Local Link version loi")
            self.reset_link_set()
            # time.sleep(1)


    # def write_update_link_to_data_base(self):
    #     # try:
    #     #     LinkVersion.remove_all()
    #     # except:
    #     #     print("Remove loi .................")

    #     self.link_version += 1
    #     self.count += 1

    #     # start_time = time.time()
    #     for link in self.link_set:
    #         src = link.get_id_src()
    #         dst = link.get_id_dst()
    #         # print("chay lan thu", self.count)
    #         weight = link.find_link_cost()

    #         delay = weight[0]
    #         link_utilization = weight[1]
    #         packet_loss = weight[2]
    #         byte_sent = weight[3]
    #         byte_received = weight[4]

    #         overhead = (byte_sent + byte_received) / 2

    #         if (overhead > 6):
    #             ratio_overhead = (overhead - 6)/6
    #         else:
    #             ratio_overhead = 0

    #         temp_data = {"src": src,
    #                     "dst": dst,
    #                     "delay": float(delay),
    #                     "linkUtilization": float(link_utilization),
    #                     "packetLoss": float(packet_loss),
    #                     "IpSDN": self.ip_local,
    #                     "overhead": float(overhead),
    #                     "ratio_overhead": float(ratio_overhead),
    #                     "byteSent": float(byte_sent),
    #                     "byteReceived": float(byte_received)
    #         }
    #         try:
    #             data_search = { 'src': temp_data['src'], 'dst': temp_data['dst'] }
    #             # print("INSERT LINK VERSION")
    #             if LinkVersion.is_data_exit(data_search=data_search):
    #                 LinkVersion.update_many(data_search, temp_data)
    #             else:
    #                 LinkVersion.insert_data(data=temp_data)
    #             # print("Ghi vao local may nay thanh cong")

    #             # ghi vao ccdn de thong ke
    #             self.write_ccdn(temp_data)
    #         except:
    #             print("--------------- Write Local Link version loi")
    #         self.reset_link_set()
    #         # time.sleep(1)

    def write_ccdn(self, temp_data):
        # Get data from local and upload to ccdn database
        url_ccdn = "http://" + self.ip_ccdn + ":5000/write_full_data/"
        requests.post(url_ccdn, data=json.dumps({'link_versions': temp_data}))
        return 

    def write_W_SDN(self, num_W):
        try:
            data = LinkVersion.get_multiple_data()
            for ip in random.sample(self.ip_remote, num_W):
                # print('ghi vao ip: ', ip)
                url = "http://" + ip + ":5000/write_link_version/"
                requests.post(url, data=json.dumps({'link_versions': data}))
                # print("Thanh cong")
        except:
            print("flask Goi nhieu SDN loiiiiiiiiiiiiiiiiiiiii")
