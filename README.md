# 🗺️ Scenario simulation Autoware

This project implements and validates autonomous driving scenarios using Autoware and Scenario Simulator V2.  
The objective was to test the ego vehicle behavior in interactive traffic situations with multiple NPC vehicles and parameterized scenario configurations.

The scenario contains:
- 1 Ego vehicle
- 2 NPC vehicles
- Trigger-based traffic interactions
- Parameterized spawn positions
- 100 automated simulation iterations

The scenario was parameterized using `ScenarioModifiers` in the YAML file.

yaml
ScenarioModifiers:
  ScenarioModifier:
    - { name: EGO_S, start: 10, step: 5, stop: 30 }
    - { name: NPC1_S, start: 5, step: 3, stop: 17 }
    - { name: NPC2_S, start: 3, step: 7, stop: 24 }

To run the code in docker:

ros2 launch scenario_test_runner scenario_test_runner.launch.py architecture_type:=awf/universe record:=false scenario:='/autoware_map/scenarios/scenario_hea1.yaml' sensor_model:=sample_sensor_kit vehicle_model:=sample_vehicle output_directory:='/autoware_map' global_real_time_factor:=1.0  use_sim_time:=true global_frame_rate:=5.0 global_timeout:=360 initialize_duration:=360 

-------------------------------------------------------------

# 🗺️ Autoware Autonomous Mapping

This project implements an autonomous mission planning for Autoware Ego with 4 goal points

To set up mapping process we have to run $ ros2 launch my_robot_controller car_nav.launch.py

Files that were added are:

autoware_terminal.sh

src/my_robot_controller/my_robot_controller/aw_navigation.py

src/my_robot_controller/launch/car_nav.launch.py

-------------------------------------------------------------

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
