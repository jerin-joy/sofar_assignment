#!/usr/bin/env python

## @package sofar_assignment
# \file vrep_interface.py
# \brief Node that acts as a user interface of the coppeliasim 
# environment.
# \author Jerin Joy, Niva Binesh, Yeshwanth Guru Krishnakumar
# \date 2022-07-10
#
# \details
#
# Description:
#
# This node acts as a user interface to the coppeliasim 
# environment that executes pick and place operation of 
# parts coming in a conveyor.
#
##

import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Int32
from threading import Thread
from sofar_assignment.srv import RandomSpawn

rospy.init_node('vrep_interface', anonymous=True)

##
# \brief Status Callback
# \param data
# 
# Prints the object status.
##

def statusCallback(data):
    rospy.loginfo("%s", data.data)

##
# \brief Spawn Callback
# \param data
# 
# Prints the status of the spawned objects
##

def spawnCallback(data):
    rospy.loginfo("%s spawned ", data.data)

##
# \brief Random Spawn Client
# \param x, y
# 
# Obtains the random number from the random spawn server.
##

def random_spawn_client(x, y):
    rospy.wait_for_service('spawn_server')
    try:
        random_spawn = rospy.ServiceProxy('spawn_server', RandomSpawn)
        resp1 = random_spawn(x, y)
        return resp1.x
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

##
# \brief Sends random number
# \param None
# 
# Publishes the random number to /pubRandom topic
##

def sendRandomNumber():
    rate = rospy.Rate(1) # 1hz
    pub_random = rospy.Publisher('pubRandom', Int32, queue_size=10)
    while not rospy.is_shutdown():
        pub_random.publish(int(random_spawn_client(0,3)))
        rate.sleep()

##
# \brief Call subscribers
# \param None
# 
# Subscribes to various topics.
##

def callSubscribers():
    rospy.Subscriber("spawnerDetails", String, spawnCallback)
    rospy.Subscriber("objectStatus", String, statusCallback)
    rospy.Subscriber("objectCounter", String, statusCallback)

##
# \brief User Interface
# \param None
# 
# Acts as the user interface for the coppeliasim environment.
##

def user_interface():
    # rospy.init_node('vrep_interface', anonymous=True)
    pub_start = rospy.Publisher('startSimulation', Bool, queue_size=10)
    pub_stop = rospy.Publisher('stopSimulation', Bool, queue_size=10)
    # pub_random = rospy.Publisher('pubRandom', Int32, queue_size=10)
    callSubscribers()
        
    rate = rospy.Rate(10) # 10hz  

    x = int(input("\nPress 1 to start the simulation "))
    while not rospy.is_shutdown():
        # pub_random.publish(int(random_spawn_client(0,3)))
        if (x == 1):
            rospy.loginfo("Simulation Started at %s", rospy.get_time())
            pub_start.publish(True)
            rate.sleep()

            x = int(input("\nPress 0 to stop the simulation "))
            
        else:
            rospy.loginfo("Simulation Stopped at %s", rospy.get_time())
            pub_stop.publish(False)
            x = int(input("\nPress 1 to start the simulation "))

if __name__ == '__main__':
    try:
        t1 = Thread(target = sendRandomNumber)
        t2 = Thread(target = user_interface)
        t1.start()
        t2.start()
        t2.join()
        # user_interface()
    except rospy.ROSInterruptException:
           pass