import rospy
from std_msgs.msg import String 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
import time 
import urllib
import urllib2
import datetime
import thread
import csv

#The data logger should be able to record and transmit
#the VUT’s time, location, speed, brake position, gear position, steering angle and motor
#RPM of e2o, at all points in addition to object/ signal recognition time, systems actuation
#time on a second by second basis.
output1 = '0' 
output2 = '0'
vel = '0' 
steer= '0' 
gear_pos= '0'
brake_pos= '0' 
sampling_rate = '5'          #don't use fraction and no. of time data will be uploaded per 5 second

def callback_gps(navsat):
	global output1
	global output2
	
	output1 = navsat.latitude
	output2 = navsat.longitude

def callback_vel(msg):
	global vel
		
	vel = msg.linear.x
	
def callback_can(msg):
	global steer       #all three should be taken from mahindra_can_final.py in twist form
	global gear_pos 
	global brake_pos    
	steer = msg.linear.x      # msg.linear.x for steering angle, msg.linear.y for gear position, msg.linear.z for brake position 
	gear_pos = msg.linear.y		# gear_pos = 1 then Neutral, gear_pos = 2 then Forward, gear_pos = 3 then Backward
	brake_pos = msg.linear.z

def callback4(data):
	global output4
	output4 = data.data

def callback5(data):
	global output5
	output5 = data.data
        
def  listener():
	rospy.init_node('listener',anonymous = True)
	rospy.Subscriber("/gps/filtered", NavSatFix, callback_gps)
	rospy.Subscriber("velocity_can", Twist, callback_vel)
	rospy.Subscriber("can2", Twist, callback_can)              # for the second topic from can
	rospy.Subscriber("chatter4", String, callback4)
	rospy.Subscriber("chatter5", String, callback5)
	rospy.spin()
def url_send() :
	global output1  
	global output2  
	global vel  
	global steer  
	global gear_pos
	global brake_pos_pos 
	global sampling_rate
	fname = datetime.datetime.now()
	with open(str(fname)+'.csv','wb') as csvfile:
		writer= csv.writer(csvfile , delimeter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['time', 'lati', 'longi', 'speed', 'steer_angle', 'gearposition', 'brakeposition' ])
		while True:
			try:
				url = 'http://shubhagrawal.in/agv_new.php?'
				rq = ""
				rq = url + 'lati=' + output1 + '&longi=' + output2 + '&speed=' + vel + '&steer_angle=' + steer + '&gearposition=' + gear_pos + '&brakeposition=' + brake_pos + '&mode=' + '0'  
				req = urllib2.Request(rq)
				response = urllib2.urlopen(req)
				now=datetime.datetime.now()
				print response
				writer.writerow([now.isoformat(), output1, output2, vel, steer, gear_pos, brake_pos])
				time.sleep(5000/sampling_rate)
			except httplib.BadStatusLine:
				pass
if __name__ == '__main__' :
	thread.start_new_thread( url_send , ())
	listener()	

