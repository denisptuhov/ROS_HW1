#! /usr/bin/python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleFollowerNode:
    def __init__(self):
        rospy.init_node('turtle_follower_node', anonymous=True)

        self.follower_speed = rospy.get_param('~follower_speed', 1.0)

        rospy.Subscriber('/turtle1/pose', Pose, self.turtle1_pose_callback)
        rospy.Subscriber('/turtle2/Pose', Pose, self.turtle2_pose_callback)

        self.cmd_vel_pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        

        self.turtle1_pose = Pose()
        self.turtle2_pose = Pose()

    def turtle1_pose_callback(self, data):
        self.turtle1_pose = data

        transform = self.calculate_transform()

        cmd_vel = self.generate_cmd_vel(transform)

        self.cmd_vel_pub.publish(cmd_vel)

    def turtle2_pose_callback(self, data): 
        self.turtle2_pose = data

    def calculate_transform(self):
        transform = Twist()
        transform.linear.x = self.turtle1_pose.x - self.turtle2_pose.x
        transform.linear.y = self.turtle1_pose.y - self.turtle2_pose.y
        transform.angular.z = self.turtle1_pose.theta - self.turtle2_pose.theta
        return transform

    def generate_cmd_vel(self, transform):
        cmd_vel = Twist()
        cmd_vel.linear.x = self.follower_speed * transform.linear.x
        cmd_vel.linear.y = self.follower_speed * transform.linear.y
        cmd_vel.angular.z = self.follower_speed * transform.angular.z
        return cmd_vel

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    follower_node = TurtleFollowerNode()
    follower_node.run()
