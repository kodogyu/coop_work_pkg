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

        self.br = CvBridge()
        self.img = np.zeros((800, 480))
        self.image_dir = f"{os.environ['HOME']}/ros2_ws/src/coop_work_pkg/images/"
        self.image_name = "drone_image.pgm"

    def image_sub_callback(self, msg):
        current_frame = self.br.imgmsg_to_cv2(msg)
        self.img = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.get_logger().info("image received")

        cv2.imshow("camera", self.img)
        cv2.waitKey(1)

    def drone_image_capture_callback(self, request, response):
        # receive the request message
        self.get_logger().info(f'Incoming request\ndata: {request.data}')

        if request.data:
            # save an image
            response.message = os.path.join(self.image_dir, self.image_name)  # full image path
            response.success = cv2.imwrite(response.message, self.img)
            if response.success:
                self.get_logger().info(f'saved file name: {response.message}')
        else:
            response.message = ""
            response.success = False
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
