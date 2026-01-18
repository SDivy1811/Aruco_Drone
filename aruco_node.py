#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__('aruco_detector_node')
        
        # Initialize CvBridge
        self.bridge = CvBridge()
        
        # Subscribe to the camera topic
        self.subscription = self.create_subscription(
            Image,
            '/world/aruco/model/x500_depth_0/link/camera_link/sensor/IMX214/image',
            self.image_callback,
            10
        )
        
        # ArUco dictionary and parameters
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
        self.get_logger().info('ArUco Detector Node started')
        self.get_logger().info(f'Subscribed to: {self.subscription.topic_name}')
    
    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Convert to grayscale for ArUco detection
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect ArUco markers
            corners, ids, rejected = self.aruco_detector.detectMarkers(gray)
            
            # Draw detected markers
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)
                
                # Log detected marker IDs
                marker_ids = ids.flatten().tolist()
                self.get_logger().info(f'Detected markers: {marker_ids}')
                
                # Draw marker axes (optional, requires camera calibration)
                # If you have camera matrix and distortion coefficients, uncomment:
                # for i in range(len(ids)):
                #     cv2.drawFrameAxes(cv_image, camera_matrix, dist_coeffs, 
                #                      rvecs[i], tvecs[i], 0.1)
            
            # Display the image with detected markers
            cv2.imshow('ArUco Marker Detection', cv_image)
            cv2.waitKey(1)
            
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')
    
    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    
    node = ArucoDetectorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()