#!/usr/bin/env python
import sys
import cv2
import rospy
from dynamic_reconfigure.server import Server
from lane_detection import LaneDetection
from line_detection.cfg import LineDetectionConfig
import numpy as np
###############################################################################
# Chicago Engineering Design Team
# Hue filter node
#
# filters out all pixels outside of hue range (self.hue_low, self.hue_high)
#
# @author Basheer Subei
# @email basheersubei@gmail.com


class HSVFilter(LaneDetection):

    def __init__(self, namespace, node_name):
        LaneDetection.__init__(self, namespace, node_name)

    # this is what gets called when an image is received
    def image_callback(self, ros_image):

        cv2_image = self.ros_to_cv2_image(ros_image)
        if self.use_roi:
            roi = self.get_roi(cv2_image)
        else:
            roi = cv2_image

        # convert from BGR to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        green_min = np.array([self.hue_low, self.saturation_low, self.value_low])
        green_max = np.array([self.hue_high, self.saturation_high, self.value_high])

        mask = cv2.inRange(hsv, green_min, green_max)
        inverted_mask = cv2.bitwise_not(mask)

        filtered_image = cv2.bitwise_and(np.dstack((inverted_mask, inverted_mask, inverted_mask)), hsv)
        final_image = cv2.cvtColor(filtered_image, cv2.COLOR_HSV2BGR)

        final_image_message = self.cv2_to_ros_message(final_image)
        # just a hack to make published messages have same timestamps,
        # used for message_filter
        final_image_message.header.stamp = ros_image.header.stamp

        self.line_image_pub.publish(final_image_message)

    # end image_callback()


def main(args):
    node_name = "hsv_filter"
    namespace = rospy.get_namespace()

    # create a HistogramCalculator object
    hf = HSVFilter(namespace, node_name)

    # start the line_detector node and start listening
    rospy.init_node("hsv_filter", anonymous=True)

    # starts dynamic_reconfigure server
    srv = Server(LineDetectionConfig, hf.reconfigure_callback)
    rospy.spin()

if __name__ == '__main__':
    main(sys.argv)
