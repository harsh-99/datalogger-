import urllib
import urllib2 
import time

while True:
	url = 'http://shubhagrawal.in/agv_new.php?'
	rq = ""
	rq = url + 'lati=' + '53.25' + '&longi=' + '29' + '&speed=' + '0' + '&heading=' + '0' + '&gearposition=' + '0' + '&brakeposition=' + '0' + '&mode=' + '0'  
	req = urllib2.Request(rq)
	#response = urllib2.urlopen(req)
	#print response
	time.sleep(1)
