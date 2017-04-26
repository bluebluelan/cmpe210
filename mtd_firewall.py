import urllib2
import urllib
import json
import time
import httplib

#PARAMETER
ip_protect = '10.0.0.8'
switch_protect = "00:00:00:00:00:00:00:02"
controller_ip = '192.168.56.102'
threshold = 20


flowSwid = {}
flowPair = {}
ip_dst = ''
ip_src = ''
flowCount =1
blockflag = False
pcnt = 0

  
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
        print ret
        conn.close()
        return ret
  
pusher = StaticFlowPusher(controller_ip)
  
flow1 = {
    'switch':str(switch_protect),
    "name":"flow_mod_1",
    "cookie":"0",
    "priority":"2",
    "in_port":"4",
    #"eth_type":"0x0800",
    #"ip_proto":"0x01",
    #"ipv4_src":"10.0.0.1",
    #"eth_src":"8e:df:b9:16:76:99",
    #"icmpv4_type":"8",
    "active":"true",
    #"actions":"output=1,set_field=eth_dst->d6:2f:6e:87:24:51,set_field=ipv4_dst->10.0.0.5"
    }
pusher.set(flow1)
#pusher.set(flow2)


def statDaemon(d):
	#print d
	try:
		if str(d['match']['ipv4_dst']) == ip_protect:
			fPKey = str(d['match']['ipv4_src'])+"-"+str(d['match']['ipv4_dst'])
			if fPKey not in flowPair:
				flowPair[fPKey]=[]
				flowPair[fPKey].append(int(d['packetCount']))
				flowPair[fPKey].append(int(d['match']['in_port']))
			print d['packetCount']+"\n"
			flowPair[fPKey][0] = int(d['packetCount'])
			print flowPair[fPKey][0]
			flowSwid[switch_protect] = flowPair
	except:
		pass

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
#curl -X GET http://192.168.1.68:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:02/json  
#curl -X DELETE -d '{"name":"block_icmp_01"}' http://192.168.1.68:8080/wm/staticflowpusher/json
"""
initflag = True
while 1:
	response = urllib2.urlopen('http://192.168.56.102:8080/wm/core/switch/all/flow/json')
	html = response.read()
	# parse response as json
	jsondata = json.loads(html)
	for data in jsondata:
		#get the key from the dict object
		#print "+++++++++++++++++++ FIND HOST +++++++++++++++++++++"
		for d in jsondata[data]["flows"]:
			#print str(d)+"\n"
			statDaemon(d)
	print flowSwid#[switch_protect]
	
	for flowPair in flowSwid[switch_protect]: 
		#print flowSwid[switch_protect][flowPair][0]
		try:
			if flowSwid[switch_protect][flowPair][0] > threshold:
				print "icmp ddos detect!\n"

				#sss=combineFlowEntry_icmpblock(flowSwid[switch_protect][flowPair][1],switch_protect)
				#flow1["in_port"]=str(flowSwid[switch_protect][flowPair][1])
				#response=urllib2.urlopen("http://192.168.56.102:8080/wm/staticflowpusher/json", sss)
				#html = response.read()
				# parse response as json
				jsondata = json.loads(html)
				flow1["switch"]=str(switch_protect)
				#pusher.set(flow1)
		except:
			pass
	response.close()
	time.sleep(5)
