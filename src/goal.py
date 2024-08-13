#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

current_pose = Pose()

def callback(data):
    global current_pose
    current_pose = data

def move_to_goal(x_goal, y_goal):
    rospy.init_node('move_to_goal', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    
    rate = rospy.Rate(10)

    goal_pose = Pose()
    goal_pose.x = x_goal
    goal_pose.y = y_goal

    vel_msg = Twist()

    while not rospy.is_shutdown():
        # distance = math.sqrt(math.pow((goal_pose.x - current_pose.x), 2) + math.pow((goal_pose.y - current_pose.y), 2))
        distance = math.sqrt((goal_pose.x - current_pose.x)**2 + (goal_pose.y - current_pose.y)**2)
        vel_msg.linear.x = 1.5 * distance

        angle_to_goal = math.atan2(goal_pose.y - current_pose.y, goal_pose.x - current_pose.x)
        angle_diff = angle_to_goal - current_pose.theta
        vel_msg.angular.z = 4.0 * angle_diff

        if distance < 0.01:
            vel_msg.linear.x=0
            vel_msg.angular.z=0
            pub.publish(vel_msg)
            break

        pub.publish(vel_msg)
        rate.sleep()

if __name__ == "__main__":
    x_goal = 8
    y_goal = 8
    move_to_goal(x_goal, y_goal)