#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class TopicsQuiz:
    def __init__(self):
        rospy.init_node('topics_quiz_node')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        self.move = Twist()
        rospy.spin()

    def callback(self, msg):
        # Indexurile depind de senzor, dar uzual: 0=dreapta, 360=fata, 719=stanga
        # Luăm valorile centrale pentru siguranță
        fata = msg.ranges[len(msg.ranges)/2]
        dreapta = msg.ranges[0]
        stanga = msg.ranges[-1]

        if fata > 1.0:
            self.move.linear.x = 0.2
            self.move.angular.z = 0.0
        
        if fata < 1.0:
            self.move.linear.x = 0.0
            self.move.angular.z = 0.3 # Turn left

        if dreapta < 1.0:
            self.move.linear.x = 0.0
            self.move.angular.z = 0.3 # Turn left

        if stanga < 1.0:
            self.move.linear.x = 0.0
            self.move.angular.z = -0.3 # Turn right

        self.pub.publish(self.move)

if __name__ == '__main__':
    try:
        TopicsQuiz()
    except rospy.ROSInterruptException:
        pass
