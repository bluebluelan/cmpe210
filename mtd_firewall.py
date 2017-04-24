import urllib2
import urllib
import json
import time

#PARAMETER
ip_protect = '10.0.0.8'
switch_protect = "00:00:00:00:00:00:00:02"
threshold = 200


flowSwid = {}
flowPair = {}
ip_dst = ''
ip_src = ''
flowCount =1
blockflag = False
pcnt = 0

def statDaemon(d):
	#print d
	try:
		if str(d['match']['ipv4_dst']) == ip_protect:
			fPKey = str(d['match']['ipv4_src'])+"-"+str(d['match']['ipv4_dst'])
			if fPKey not in flowPair:
				flowPair[fPKey]=[]
				flowPair[fPKey].append(int(d['packetCount']))
				flowPair[fPKey].append(int(d['match']['in_port']))
			flowPair[fPKey][0] = int(d['packetCount'])
			flowSwid[switch_protect] = flowPair
	except:
		pass

def combineFlowEntry(in_port, switch_protect):
	sss  = '{"switch":"'+str(switch_protect)+'", '
	sss += '"name":"block_icmp_'+str(flowCount)+'", '
	sss += ' "cookie":"0", "priority":"32768", '
	sss += '"in_port":"'+str(in_port)+'", '
	sss += '"icmpv4_type":"8", "active":"true"}'
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


#"curl -d '{"switch": "00:00:00:00:00:00:00:01", "name":"flow-mod-1", "cookie":"0", "priority":"32768", "ingress-port":"1","active":"true", "actions":"output=2"}' http://<controller_ip>:8080/wm/staticflowpusher/json "

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


#sss = '{"switch":"00:00:00:00:00:00:00:02", "name":"block_icmp_01", "cookie":"0", "priority":"32768", "in_port":"3", "icmpv4_type":"8", "active":"true"}'
#sss = '{"switch":"00:00:00:00:00:00:00:02", "name":"block_icmp_1",  "cookie":"0", "priority":"32768", "in_port":"3", "icmpv4_type":"8", "active":"true"}'
while 1:
	response = urllib2.urlopen('http://192.168.1.68:8080/wm/core/switch/all/flow/json')
	html = response.read()
	# parse response as json
	jsondata = json.loads(html)
	#swid = jsondata[]
	for data in jsondata:
		#get the key from the dict object
		#print "+++++++++++++++++++ FIND HOST +++++++++++++++++++++"
		for d in jsondata[data]["flows"]:
			#if the key is something we want, just print it
			#print d
			statDaemon(d)
	print flowSwid[switch_protect]
	for flowPair in flowSwid[switch_protect]: 
		#print flowSwid[switch_protect][flowPair][0]
		try:
			if flowSwid[switch_protect][flowPair][0] > threshold:
				print "icmp ddos detect!\n"
				sss=combineFlowEntry(flowSwid[switch_protect][flowPair][1],switch_protect)
				#print sss
				response=urllib2.urlopen("http://192.168.1.68:8080/wm/staticflowpusher/json", sss)
				html = response.read()
				# parse response as json
				jsondata = json.loads(html)
				#print jsondata
		except:
			pass
	response.close()
	time.sleep(5)
