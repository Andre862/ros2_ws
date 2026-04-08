# 🗺️ TurtleBot3 Autonomous Mapping (ROS2)

This project implements an autonomous mapping system for TurtleBot3 using ROS 2, Gazebo simulation, and Cartographer SLAM.

To set up mapping process we have to run $ ros2 launch my_robot_controller mapping.launch.py command. It opens 3 files at one. Those are

my_robot_controller/launch/turtlebot3_world.launch.py

turtlebot3_cartographer/launch/cartographer.launch.py

my_robot_controller/mapping

-------------------------------------------------------------

# 🗺️ TurtleBot Autonomous Navigation (ROS2)

## 📌 Overview
This project implements autonomous navigation for a TurtleBot in a custom map using ROS2 and Nav2.

## 🚀 Launch File
The launch file starts:
- Simulation with custom map
- Nav2 navigation stack
- Mission script node

To launch:

ros2 launch my_robot_controller turtlebot3_navigation.launch.py 
