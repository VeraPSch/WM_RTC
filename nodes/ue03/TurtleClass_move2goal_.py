#!/usr/bin/env python3
# --- TurtleClass_move2Goal.py ------
# Version vom 23.11.2020 by OJ
# ----------------------------
# from
# --- P3_V4_TurtleClass_move2goal.py ------
# Version vom 22.10.2019 by OJ
# Basiert auf der Loesung aus dem Turtlesim Tutorial
# http://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
#
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBotClass:

    def __init__(self):
        # globale Klassen-Variablen instanzieren
        self.pose = Pose()
        self.goal = Pose()
        self.vel_msg = Twist()

        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 5)
        self.pose.y = round(self.pose.y, 5)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def set_linear_vel(self, goal_pose, constant=0.5, lin_max=1.0):
        lin_vel = constant * self.euclidean_distance(goal_pose)
        if lin_vel > lin_max:
            lin_vel = lin_max  # Maximum begrenzen
        self.vel_msg.linear.x = lin_vel
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def set_angular_vel(self, goal_pose, constant=1.0, ang_max=1.5):
        ang_vel = constant * (self.steering_angle(goal_pose) - self.pose.theta)
        if(ang_vel > ang_max):
            ang_vel = ang_max
        self.vel_msg.angular.z = ang_vel
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0

    def getGoalFromUser(self):
        self.stop_robot()
        self.goal.x = eval(input("Set your x goal: "))
        self.goal.y = eval(input("Set your y goal: "))

    def start_info(self):
        # Debug Info
        rospy.loginfo("Start Pose is %f %f", self.pose.x, self.pose.y)
        rospy.loginfo("Goal is       %f %f", self.goal.x, self.goal.y)
        rospy.loginfo("Distannce to Goal is  %f ",
                      self.euclidean_distance(self.goal))
        rospy.loginfo("SteeringAngle to Goal is  %f ",
                      self.steering_angle(self.goal))
        input("Hit any Key to start")

    def pose_speed_info(self):
        rospy.loginfo("Pose is %s %s",
                      round(self.pose.x, 4),
                      round(self.pose.y, 4))
        rospy.loginfo("Speed is x: %s  theta: %s",
                      round(self.vel_msg.linear.x, 4),
                      round(self.vel_msg.angular.z, 4))

    def stop_robot(self):
        # Stopping our robot after the movement is over.
        rospy.loginfo(" ######  Goal reached, Stop Robot #######")
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)

    def goal_reached(self, distance_tolerance=0.1):
        if self.euclidean_distance(self.goal) < distance_tolerance:
            return True
        else:
            return False

    def move2goal(self):
        # Moves the turtle to the goal
        
        while not self.goal_reached():
            # Linear velocity in the x-axis.
            self.set_linear_vel(self.goal)
            # Angular velocity in the z-axis.
            self.set_angular_vel(self.goal)

            # Publishing our vel_msg
            self.velocity_publisher.publish(self.vel_msg)
            # Publish at the desired rate.
            self.rate.sleep()
            # debug Info
            self.pose_speed_info()

        self.stop_robot()  # when goal is reached
        exit()


if __name__ == '__main__':
    try:
        turtle1 = TurtleBotClass()
        turtle1.getGoalFromUser()
        turtle1.start_info()
        turtle1.move2goal()
    except rospy.ROSInterruptException:
        pass
