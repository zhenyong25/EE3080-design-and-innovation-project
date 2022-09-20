cmake_minimum_required(VERSION 2.8.3)
project(edclient)
find_package(catkin REQUIRED)
catkin_package()
catkin_python_setup()
install(PROGRAMS bin/edclient bin/cfheadless
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
