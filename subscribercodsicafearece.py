#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    # Luăm câteva puncte cheie din scanarea laser
    # dist_fata e la mijlocul array-ului de date
    dist_fata = msg.ranges[len(msg.ranges)//2]
    dist_dreapta = msg.ranges[0]
    dist_stanga = msg.ranges[-1]
    
    rospy.loginfo("--- Citiri Laser ---")
    rospy.loginfo(f"Fata: {dist_fata:.2f}m")
    rospy.loginfo(f"Dreapta: {dist_dreapta:.2f}m")
    rospy.loginfo(f"Stanga: {dist_stanga:.2f}m")
    rospy.loginfo("--------------------")

def listener():
    # Inițializăm nodul de subscriber
    rospy.init_node('subscriber_quiz_node', anonymous=True)
    
    # Ne abonăm la topicul /scan
    rospy.Subscriber("/scan", LaserScan, callback)
    
    rospy.loginfo("Subscriber-ul a pornit și așteaptă date...")
    
    # Menținem nodul activ până la oprire
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
