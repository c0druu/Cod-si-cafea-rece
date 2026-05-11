#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from cafea_test2.srv import Mesajul, MesajulResponse

obstacle_detected = False

def scan_callback(msg):
    global obstacle_detected

    front_ranges = msg.ranges[0:20] + msg.ranges[-20:]  
    valid_ranges = []

    for distance in front_ranges:
        if distance > 0.0 and distance < float ('inf'):
            valid_ranges.append(distance)

    if len(valid_ranges)  == 0:
       obstacle_detected = False
       return
    
    min_distance = min(valid_ranges)
    if min_distance < 0.7:
        obstacle_detected = True
    else:
        obstacle_detected = False

def handle_check_obstacle(req):
    rospy.loginfo(f"Serverul a primit cerere pentru patrat de {req.side}m, de {req.repetitions} ori")
    return MesajulResponse(obstacle_detected)

rospy.init_node("server_cafea")
rospy.Subscriber("/scan", LaserScan, scan_callback)
service = rospy.Service("/check_obstacle", Mesajul, handle_check_obstacle)
rospy.loginfo("Serverul a pornit.")
rospy.spin() 
