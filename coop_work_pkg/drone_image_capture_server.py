import rclpy
from rclpy.node import Node

from std_srvs.srv import SetBool
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2
import numpy as np
import os


class MinimalService(Node):

    def __init__(self):
        super().__init__('drone_image_capture_server')
        self.sub = self.create_subscription(Image,
                                            'typhoon_h480_ros/camera/image_raw',
                                            self.image_sub_callback,
                                            10)
        self.srv = self.create_service(SetBool,
                                       'capture_drone_image',
                                       self.drone_image_capture_callback)

        self.brdge = CvBridge()
        self.image = np.zeros((800, 480))
        self.image_dir = f"{os.environ['HOME']}/ros2_ws/src/coop_work_pkg/images/"
        self.image_name = "drone_image"
        self.image_number = 0
        self.image_extension = ".png"

    def image_sub_callback(self, msg):
        current_frame = self.bridge.imgmsg_to_cv2(msg)
        self.image = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.get_logger().info("image received")

        cv2.imshow("camera", self.image)
        cv2.waitKey(1)

    def drone_image_capture_callback(self, request, response):
        # receive the request message
        self.get_logger().info(f'Incoming request\ndata: {request.data}')
        response.message = ""
        response.success = False
                
        if request.data:
            # Save an image
            # full image path
            response.message = os.path.join(self.image_dir, self.image_name + str(self.image_number) + self.image_extension)
            response.success = cv2.imwrite(response.message, self.image)
            if response.success:
                # image saving success
                self.get_logger().info(f'saved file name: {response.message}')
                self.image_number += 1
            else:
                # image saving fail
                self.get_logger().info('file saving Failed')

        self.get_logger().info(f'Request process: {response.success}')
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
