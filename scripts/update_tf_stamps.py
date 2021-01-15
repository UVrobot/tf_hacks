#!/usr/bin/env python

# A script that listens to /tfout and tf_staticout topics,
# updates the timestamps for all TFs and relays them to /tf and tf_static

import rospy
from tf2_msgs.msg import TFMessage

tf_pub = None
tfs_pub = None

def tfcb(msg):
    for i in range(len(msg.transforms)):
        msg.transforms[i].header.stamp = rospy.Time.now()
    tf_pub.publish(msg)

def tfscb(msg):
    for i in range(len(msg.transforms)):
        msg.transforms[i].header.stamp = rospy.Time.now()
    tfs_pub.publish(msg)

def init():
    global tf_pub, tfs_pub
    rospy.init_node("tf_hack")

    tf_sub = rospy.Subscriber("tfout", TFMessage, tfcb)
    tfs_sub = rospy.Subscriber("tf_staticout", TFMessage, tfscb)

    tf_pub = rospy.Publisher("tf", TFMessage, queue_size=1)
    tfs_pub = rospy.Publisher("tf_static", TFMessage, queue_size=1)

    rospy.spin()

if __name__ == "__main__":
    init()

