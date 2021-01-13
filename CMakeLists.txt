cmake_minimum_required(VERSION 3.0.2)
project(tf_hacks)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  tf
  tf2_msgs
)

catkin_package()

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
