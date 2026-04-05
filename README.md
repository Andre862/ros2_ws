# 🗺️ TurtleBot3 Autonomous Mapping (ROS 2)

This project implements an autonomous mapping system for TurtleBot3 using ROS 2, Gazebo simulation, and Cartographer SLAM.

To set up mapping process we have to run $ ros2 launch my_robot_controller mapping.launch.py command. It opens 3 files at one. Those are

my_robot_controller/launch/turtlebot3_world.launch.py

turtlebot3_cartographer/launch/cartographer.launch.py

my_robot_controller/mapping
