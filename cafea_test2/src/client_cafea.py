#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from cafea_test2.srv import Mesajul, MesajulRequest

def executa_patrat():
    rospy.init_node("client_cafea")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.wait_for_service("/check_obstacle")
    
    serviciu = rospy.ServiceProxy("/check_obstacle", Mesajul)
    
  
    latura = 1.0 # float64
    repetari = 1 # int32
    
    viteza = 0.2
    timp_latura = latura / viteza
    timp_rotire = 1.57 / 0.5

    for r in range(repetari):
        rospy.loginfo(f"Incepem repetarea numarul {r+1}")
        for i in range(4):
            
            raspuns = serviciu(side=latura, repetitions=repetari)
            
            if raspuns.obstacle_detected:
                rospy.logwarn("Obstacol! Nu pot face patratul!")
                pub.publish(Twist()) 
                return

            
            msg = Twist()
            msg.linear.x = viteza
            pub.publish(msg)
            rospy.sleep(timp_latura)

            
            msg = Twist()
            msg.angular.z = 0.5
            pub.publish(msg)
            rospy.sleep(timp_rotire)
            
           
            pub.publish(Twist())
            rospy.sleep(0.5)

if __name__ == "__main__":
    executa_patrat()