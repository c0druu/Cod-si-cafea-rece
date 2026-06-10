cmake_minimum_required(VERSION 3.0.2)
# Am actualizat numele proiectului pentru a corespunde cu folderul din workspace-ul tau
project(cafea_test1)

## Find catkin macros and libraries
# Am adaugat message_generation si std_msgs (necesar pentru float32 si string)
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  sensor_msgs
  std_msgs
  message_generation
)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate messages in the 'msg' folder
# Am specificat fisierul tau de mesaj
add_message_files(
  FILES
  CafeaMsg.msg
)

## Generate added messages and services with any dependencies listed here
# Mesajul tau depinde de std_msgs
generate_messages(
  DEPENDENCIES
  std_msgs
)

###################################
## catkin specific configuration ##
###################################
# Am adaugat message_runtime aici, este obligatoriu pentru executie
catkin_package(
  CATKIN_DEPENDS geometry_msgs rospy sensor_msgs std_msgs message_runtime
)

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)