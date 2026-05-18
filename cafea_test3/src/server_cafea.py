#! /usr/bin/env python3
import rospy
import actionlib
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cafea_test3.msg import MesajAction, MesajGoal, MesajFeedback, MesajResult

class CafeaActionServer(object):
    def __init__(self):
        self.cafea_feedback = MesajFeedback()
        self.cafea_result = MesajResult()
        self.cafea_takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.cafea_land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        self.cafea_cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cafea_action_server = actionlib.SimpleActionServer(
            'mesaj', MesajAction, self.cafea_goal_callback, False
        )
        self.cafea_action_server.start()
        rospy.loginfo('cafea action server started')

    def cafea_send_hover(self):
        cafea_twist = Twist()
        cafea_twist.linear.x = 0.0
        cafea_twist.linear.y = 0.0
        cafea_twist.linear.z = 0.0
        cafea_twist.angular.x = 0.0
        cafea_twist.angular.y = 0.0
        cafea_twist.angular.z = 0.0
        self.cafea_cmd_vel_pub.publish(cafea_twist)

    def cafea_send_lift(self):
        cafea_twist = Twist()
        cafea_twist.linear.z = 0.5
        self.cafea_cmd_vel_pub.publish(cafea_twist)

    def cafea_send_descend(self):
        cafea_twist = Twist()
        cafea_twist.linear.z = -0.3
        self.cafea_cmd_vel_pub.publish(cafea_twist)

    def cafea_goal_callback(self, cafea_goal):
        cafea_command = cafea_goal.command.strip().upper()
        if cafea_command in ['TAKEOFF', 'TAKEOOFF']:
            self.cafea_feedback.feedback = 'take off'
            rospy.loginfo('cafea sending takeoff')
            for _ in range(3):
                self.cafea_takeoff_pub.publish(Empty())
                rospy.sleep(0.2)

            lift_end = rospy.Time.now() + rospy.Duration(3.0)
            rate = rospy.Rate(10)
            cafea_count = 0
            while not rospy.is_shutdown() and rospy.Time.now() < lift_end:
                if self.cafea_action_server.is_preempt_requested():
                    rospy.loginfo('cafea takeoff preempted')
                    self.cafea_action_server.set_preempted()
                    return
                self.cafea_send_lift()
                cafea_count += 1
                if cafea_count % 10 == 0:
                    self.cafea_action_server.publish_feedback(self.cafea_feedback)
                rate.sleep()

            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                if self.cafea_action_server.is_preempt_requested():
                    rospy.loginfo('cafea takeoff preempted')
                    self.cafea_action_server.set_preempted()
                    return
                self.cafea_send_hover()
                self.cafea_action_server.publish_feedback(self.cafea_feedback)
                rate.sleep()
        elif cafea_command == 'LAND':
            self.cafea_feedback.feedback = 'landing'
            rospy.loginfo('cafea sending land')
            for _ in range(3):
                self.cafea_land_pub.publish(Empty())
                rospy.sleep(0.2)

            descend_end = rospy.Time.now() + rospy.Duration(4.0)
            rate = rospy.Rate(10)
            cafea_count = 0
            while not rospy.is_shutdown() and rospy.Time.now() < descend_end:
                if self.cafea_action_server.is_preempt_requested():
                    rospy.loginfo('cafea landing preempted')
                    self.cafea_action_server.set_preempted()
                    return
                self.cafea_send_descend()
                cafea_count += 1
                if cafea_count % 10 == 0:
                    self.cafea_action_server.publish_feedback(self.cafea_feedback)
                rate.sleep()

            rate = rospy.Rate(5)
            for _ in range(5):
                if self.cafea_action_server.is_preempt_requested():
                    rospy.loginfo('cafea landing preempted')
                    self.cafea_action_server.set_preempted()
                    return
                self.cafea_send_hover()
                self.cafea_action_server.publish_feedback(self.cafea_feedback)
                rate.sleep()
            self.cafea_action_server.set_succeeded(self.cafea_result)
        else:
            rospy.logwarn('cafea invalid command %s', cafea_command)
            self.cafea_action_server.set_aborted(self.cafea_result)

if __name__ == '__main__':
    rospy.init_node('cafea_server')
    CafeaActionServer()
    rospy.spin()
