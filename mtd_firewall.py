import urllib2
import urllib
import json
import time
import httplib

#PARAMETER
ip_protect = '10.0.0.8'
switch_protect = "00:00:00:00:00:00:00:03"
controller_ip = '192.168.56.102'
threshold = 5

icmp_pair = {}
flowSwid = {}
flowPair = {}
ip_dst = ''
ip_src = ''
flowCount =1
blockflag = False
pcnt = 0

flow1 = {
    'switch':str(switch_protect),
    "name":"icmp_beacon",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x01",
    "ipv4_src":"10.0.0.1",
    "icmpv4_type":"8",
    "active":"true",
    "actions":"output=4"
}
flow3 = {
    'switch':str(switch_protect),
    "name":"udp_beacon",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x11",
    "ipv4_src":"10.0.0.1",
    "active":"true",
    "actions":"output=4"
}
flow4 = {
    'switch':str(switch_protect),
    "name":"tcp_beacon",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "ipv4_src":"10.0.0.1",
    "active":"true",
    "actions":"output=4"
}
flow7 = {
    'switch':str(switch_protect),
    "name":"http_beacon",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "tp_dst":"80",
    "ipv4_src":"10.0.0.1",
    "active":"true",
    "actions":"output=4"
}
    
flow2 = {
    'switch':str(switch_protect),
    "name":"icmp_block",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x01",
    "ipv4_src":"10.0.0.1",
    "icmpv4_type":"8",
    "active":"true",
    "actions":"output=1,set_field=eth_dst->86:ee:8f:9b:8d:a8,set_field=ipv4_dst->10.0.0.5"
}
flow5 = {
    'switch':str(switch_protect),
    "name":"udp_block",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x11",
    "ipv4_src":"10.0.0.1",
    "active":"true",
    "actions":"output=1,set_field=eth_dst->86:ee:8f:9b:8d:a8,set_field=ipv4_dst->10.0.0.5"
}
flow6 = {
    'switch':str(switch_protect),
    "name":"tcp_block",
    "cookie":"0",
    "priority":"2",
    "in_port":"5",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "ipv4_src":"10.0.0.1",
    "active":"true",
    "actions":"output=in_port"
}

class StaticFlowPusher(object):
  
    def __init__(self, server):
        self.server = server
  
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
  
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
  
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
  
    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        #print ret
        conn.close()
        return ret
  
pusher = StaticFlowPusher(controller_ip)
  

#pusher.set(flow1)
#pusher.set(flow2)

#http://192.168.56.102:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:03/flow/json
#http://192.168.56.102:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:03/json
#http://192.168.56.102:8080/wm/core/staticflowpusher/list/00:00:00:00:00:00:00:03/flow/json
#http://192.168.56.102:8080/wm/core/switch/00:00:00:00:00:00:00:03/flow/json
def get_device_url(url_json):
    #print url_json
    response = urllib2.urlopen(url_json)
    html = response.read()
    # parse response as json
    jsondata = json.loads(html)
    response.close()
    return jsondata

def push_icmp_beacon(flow):
    pusher.set(flow)

def statDaemon1(d):
    #print switch_protect
    try:
        if str(d['match']['ipv4_dst']) == ip_protect:
            fPKey = str(d['match']['ipv4_src'])+"-"+str(d['match']['ipv4_dst'])
            if fPKey not in flowPair:
                flowPair[fPKey]=[]
                flowPair[fPKey].append(int(d['packetCount']))
                flowPair[fPKey].append(int(d['match']['in_port']))
            print d['packetCount']+','+d['match']['ipv4_dst']+"\n"
            flowPair[fPKey][0] = int(d['packetCount'])
            #print "haha"+str(data)
            flowSwid[switch_protect] = flowPair
    except:
        pass
def statDaemon(d):
    #print switch_protect
    try:
        if str(d['match']['ipv4_dst']) == ip_protect:
            fPKey = str(d['match']['ipv4_src'])+"-"+str(d['match']['ipv4_dst'])
            if fPKey not in flowPair:
                flowPair[fPKey]=[]
                flowPair[fPKey].append(int(d['packetCount']))
                flowPair[fPKey].append(int(d['match']['in_port']))
            print d['packetCount']+"\n"
            flowPair[fPKey][0] = int(d['packetCount'])
            #print "haha"+str(data)
            flowSwid[switch_protect] = flowPair
    except:
        pass
"""
def combineFlowEntry_icmpblock(in_port, switch_protect):
    sss  = '{"switch":"'+str(switch_protect)+'", '
    sss += '"name":"block_icmp_'+str(flowCount)+'", '
    sss += '"cookie":"0", "priority":"0", '
    sss += '"in_port":"'+str(in_port)+'", '
    sss += '"icmpv4_type":"8", "active":"true"}'
    return sss
def combineFlowEntry_icmpRedirect(in_port, switch_protect):
    sss  = '{"switch":"'+str(switch_protect)+'", '
    sss += '"name":"block_icmp_'+str(flowCount)+'", '
    sss += '"cookie":"0", "priority":"32767", '
    sss += '"in_port":"'+str(in_port)+'", '
    sss += '"icmpv4_type":"8", "active":"true", '
    sss += '"actions":"output=4, set_ipv4_dst=10.0.0.6, set_eth_dst=42:e2:25:13:22:eb"}'

    return sss
#sss = '{"switch":"00:00:00:00:00:00:00:02", "name":"block_icmp_01", "cookie":"0", "priority":"32768", "in_port":"3", "icmpv4_type":"8", "active":"true"}'
"""
#curl -X POST http://192.168.1.68:8080/wm/statistics/config/enable/json
#curl -X GET http://192.168.1.68:8080/wm/statistics/bandwidth/00:00:00:00:00:00:00:02/3/json
#curl -X GET http://192.168.1.68:8080/wm/core/switch/all/flow/json
#curl -X GET http://192.168.1.68:8080/wm/core/switch/00:00:00:00:00:00:00:02/flow/json
#curl -X GET http://192.168.1.68:8080/wm/core/switch/00:00:00:00:00:00:00:02/aggregate/json
#curl -X GET http://192.168.1.68:8080/wm/core/switch/all/aggregate/json  
#curl -X GET http://192.168.1.68:8080/wm/core/switch/all/port/json
#curl -X GET http://192.168.1.68:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:02/json  

"""
curl -X POST -d '{
    "switch":"00:00:00:00:00:00:00:03",
    "name":"block_icmp_01",
    "cookie":"0",
    "priority":"32768",
    "in_port":"1",
    "icmpv4_type":"8",
    "active":"true",
    "actions":"drop"}' http://192.168.1.68:8080/wm/staticflowpusher/json
curl -X POST -d '{
    "switch":"00:00:00:00:00:00:00:02",
    "name":"block_icmp_01",
    "cookie":"0",
    "priority":"32768",
    "in_port":"3",
    "icmpv4_type":"8",
    "active":"true"}' http://192.168.1.68:8080/wm/staticflowpusher/json
#curl -X GET http://192.168.56.102:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:03/json  
#http://192.168.56.102:8080/wm/core/switch/00:00:00:00:00:00:00:03/flow/json
#curl -X DELETE -d '{"name":"block_icmp_01"}' http://192.168.56.102:8080/wm/topology/route/00:00:00:00:00:00:00:01/1/00:00:00:00:00:00:00:02/2/json
"""
initflag = True
devicePair=[]
url_json = "http://"+controller_ip+":8080/wm/device/"
jsondata = get_device_url(url_json)
for p in jsondata:
    devicePair.append([p['mac'],p['ipv4'],0])
#print devicePair
push_icmp_beacon(flow1)
push_icmp_beacon(flow3)
#push_icmp_beacon(flow4)
push_icmp_beacon(flow7)

while 1:

    try:
        url_json = "http://"+controller_ip+":8080/wm/core/switch/"+switch_protect+"/flow/json"
        jsondata = get_device_url(url_json)

        for data in jsondata:
            #print data
            for d in jsondata[data]:
                print str(d)+"\n"
                if len(d['match']) >0: statDaemon1(d)
        print flowSwid#[switch_protect]
    except:
        pass
    #url_json = "http://"+controller_ip+":8080/wm/core/switch/"+switch_protect+"/flow/json"
    #jsondata = get_device_url(url_json)
    
   # print jsondata
    for i in jsondata["flows"]:
        #print i['priority']
        if i['priority'] == '2':
            if int(i['packetCount']) > threshold:
                print "icmp_ddos_detect"
                pusher.set(flow2)
                pusher.set(flow5)
                pusher.set(flow6)
        #for d in i:
        #    print d
       # if i["priority"] == 2:
       #     print i["packetCount"]
       # if i == 'icmp_beacon':
       #     pass
    
    time.sleep(5)
