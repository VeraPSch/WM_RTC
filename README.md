# WM_RTC
Repository für das Wahlmodul der Roboterprogrammierung mir ROS und Python und die RTC.

Connecting Turtlebot3 
$ ssh 192.... (IP Adresse der Turtle angeben über WLAN)
$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

Manuelle Steuerung
$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

Karte machen
$ roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping 

Karte speichern
$ rosrun map_server map_saver -f
/home/vera/catkin_ws/src/rtc/rtc_maps/gazebo_eigene_world_map

Navigieren 
$ roslaunch turtlebot3_navigation turtlebot3_navigation.launch
map_file:=$HOME/catkin_ws/src/rtc/rtc_maps/gazebo_eigene_world_map.yaml 
(wichtig .yaml file)
