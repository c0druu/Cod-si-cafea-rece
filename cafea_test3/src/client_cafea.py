#!/usr/bin/env python3

import rospy
import actionlib
from cafea_test3.msg import MesajAction, MesajGoal


class CafeaClient:
    def __init__(self):
        self.cafea_client = actionlib.SimpleActionClient('mesaj', MesajAction)
        rospy.loginfo('waiting for cafea action server')
        self.cafea_client.wait_for_server()

    def cafea_feedback_callback(self, cafea_feedback):
        rospy.loginfo('cafea feedback %s', cafea_feedback.feedback)

    def cafea_send_goal(self, cafea_command, cafea_wait=True):
        cafea_goal = MesajGoal()
        cafea_goal.command = cafea_command
        rospy.loginfo('sending cafea goal %s', cafea_command)
        self.cafea_client.send_goal(cafea_goal, feedback_cb=self.cafea_feedback_callback)
        if cafea_wait:
            self.cafea_client.wait_for_result()
            cafea_result = self.cafea_client.get_result()
            if cafea_result is not None:
                rospy.loginfo('cafea action finished')
            else:
                rospy.logwarn('cafea no result')
        return self.cafea_client.get_state()


def main():
    rospy.init_node('cafea_client')
    cafea_client = CafeaClient()
    cafea_client.cafea_send_goal('TAKEOFF', cafea_wait=False)
    rospy.sleep(8.0)
    cafea_client.cafea_send_goal('LAND', cafea_wait=True)


if __name__ == '__main__':
    main()
