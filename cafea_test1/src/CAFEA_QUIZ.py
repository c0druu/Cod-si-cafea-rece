#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

from cafea_test1.msg import CafeaMsg 

pub_miscare = None
pub_status_custom = None

def evalueaza_obstacole(dist_fata, dist_stanga, dist_dreapta):
    
    mesaj = CafeaMsg()
    
    mesaj.cafea_front_distance = dist_fata
    mesaj.cafea_left_distance = dist_stanga
    mesaj.cafea_right_distance = dist_dreapta
    mesaj.cafea_signature = "Cojocaru Marin-Codrut - ISB"
    

    if dist_fata < 1.0:
        mesaj.cafea_command_linear = 0.0
        mesaj.cafea_command_angular = 0.5
        mesaj.cafea_action = "Obstacol in fata - Evitare stanga"
        
    elif dist_dreapta < 1.0:
        mesaj.cafea_command_linear = 0.0
        mesaj.cafea_command_angular = 0.5
        mesaj.cafea_action = "Obstacol dreapta - Evitare stanga"
        
    elif dist_stanga < 1.0:
        mesaj.cafea_command_linear = 0.0
        mesaj.cafea_command_angular = -0.5
        mesaj.cafea_action = "Obstacol stanga - Evitare dreapta"
        
    else:
        # Traseul este liber
        mesaj.cafea_command_linear = 0.2
        mesaj.cafea_command_angular = 0.0
        mesaj.cafea_action = "Traseu liber - Inaintare"

    return mesaj

def procesare_scan(scan_data):

    d_fata = scan_data.ranges[0]
    d_stanga = scan_data.ranges[90]
    d_dreapta = scan_data.ranges[270]

    status_curent = evalueaza_obstacole(d_fata, d_stanga, d_dreapta)
    
    rospy.loginfo("[Actiune]: %s | Semnatura: %s", status_curent.cafea_action, status_curent.cafea_signature)

    pub_status_custom.publish(status_curent)

    comanda_robot = Twist()
    comanda_robot.linear.x = status_curent.cafea_command_linear
    comanda_robot.angular.z = status_curent.cafea_command_angular

    pub_miscare.publish(comanda_robot)


rospy.init_node('nod_evitare_modularizat')

pub_miscare = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

pub_status_custom = rospy.Publisher('/stare_robot', CafeaMsg, queue_size=1)

rospy.Subscriber('/scan', LaserScan, procesare_scan)

rospy.spin()

    