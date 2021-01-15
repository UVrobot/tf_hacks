#!/usr/bin/env python

# A script that listens to /tfout and tf_staticout topics,
# updates the timestamps for all TFs and relays them to /tf and tf_static

import time
import rospy
from tf2_msgs.msg import TFMessage

tf_pub = None
tfs_pub = None

ts = TFMessage()

def tfcb(msg):
    for i in range(len(msg.transforms)):
        msg.transforms[i].header.stamp = rospy.Time.now()
    tf_pub.publish(msg)

def tfscb(msg):
    global ts
    for i in range(len(msg.transforms)):
        msg.transforms[i].header.stamp = rospy.Time.now()
    ts.transforms.extend(msg.transforms)
    rm = []
    for i in range(len(ts.transforms)):
        for j in range(i-1,0,-1):
            if ts.transforms[i].header.frame_id == ts.transforms[j].header.frame_id and ts.transforms[i].child_frame_id == ts.transforms[j].child_frame_id:
                rm.append(j)
                break
    ts.transforms = [ts.transforms[i] for i in range(len(ts.transforms)) if i not in rm]

    print("Updating static tfs")
    tfs_pub.publish(ts)

def init():
    global tf_pub, tfs_pub
    rospy.init_node("tf_hack")

    tf_pub = rospy.Publisher("tf", TFMessage, queue_size=1)
    tfs_pub = rospy.Publisher("tf_static", TFMessage, queue_size=1, latch=True)
    
    time.sleep(2)

    tf_sub = rospy.Subscriber("tfout", TFMessage, tfcb)
    tfs_sub = rospy.Subscriber("tf_staticout", TFMessage, tfscb)

    rospy.spin()

if __name__ == "__main__":
    init()

