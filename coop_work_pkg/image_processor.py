import rclpy
from rclpy.node import Node

from std_srvs.srv import SetBool

import cv2
import numpy as np
import os

class ImageProcessor(Node):

    def __init__(self):
        super().__init__('image_processor')
        self.srv = self.create_service(SetBool, 
                                       "image_processor_srv", 
                                       self.image_processor_callback)
        
        self.workspace_path = f"{os.environ['HOME']}/ros2_ws/src/coop_work_pkg/"
        self.map_file = "maps/2d_map.png"
        self.yaml_file = "maps/2d_map.yaml"

        self.get_logger().info("image_processor_srv server initialized. Waiting for Request...")
        
    def image_processor_callback(self, request, response):
        message = "Failed"
        result = False
        
        self.get_logger().info(f"Request Recieved ({request.data})")
        if request.data == True:
            message, result = self.process_images()
            self.get_logger().info(f"Processing result: {result}")

            self.write_yaml_file()
            self.get_logger().info("YAML file saved")

        response.message = message
        response.success = result

        return response

    def process_images(self):
        """
        Image processing function.
        좌상단, 우상단, 우하단, 좌하단 4 장의 이미지를 붙여서
        2D 지도를 생성 & 저장
        """

        image_files = ["drone_image0.png", "drone_image1.png", "drone_image2.png", "drone_image3.png"]
        drone_images = []

        # Image read
        self.get_logger().info("Image reading...")
        for image in image_files:
            drone_image = cv2.imread(self.workspace_path + "images/" + image, cv2.IMREAD_COLOR)
            drone_images.append(drone_image)

        # Image crop
        self.get_logger().info("Image cropping...")
        image_height, image_width = drone_images[0].shape[:2]
        image_center = (image_height // 2, image_width // 2)
        
        window_height = 136
        window_width = 128

        cropped_images = []

        for drone_image in drone_images:
            cropped_image = drone_image[image_center[0] - window_height//2 : image_center[0] + window_height//2,
                                        image_center[1] - window_width//2 : image_center[1] + window_width//2,
                                        :]
            cropped_images.append(cropped_image)

        # Image concatenate
        self.get_logger().info("Image concatenating...")
        offset_height = 2  # 미세 조정을 위한 수직 offset 높이 (pixels)
        offset_vert_width = 5  # 미세 조정을 위한 수평 offset 너비 (pixels)
        offset_array = np.zeros((offset_height, window_width, 3)).astype('uint8')
        offset_array_vert = np.zeros((window_height + offset_height, offset_vert_width, 3)).astype('uint8')

        cropped_image0 = np.concatenate((offset_array, cropped_images[0]), axis=0)  # 좌상단 이미지 위에 offset array 추가
        cropped_image1 = np.concatenate((cropped_images[1], offset_array), axis=0)  # 우상단 이미지 아래에 offset array 추가
        cropped_image2 = np.concatenate((cropped_images[2], offset_array), axis=0)  # 우하단 이미지 아래에 offset array 추가
        cropped_image3 = np.concatenate((offset_array, cropped_images[3]), axis=0)  # 좌하단 이미지 위에 offset array 추가

        # top 좌우 사진을 병합하고 오른쪽에 offset array 추가
        concat_image_top = np.concatenate((cropped_image0, cropped_image1, offset_array_vert), axis=1)
        # bottom 좌우 사진을 병합하고 왼쪽에 offset array 추가
        concat_image_bottom = np.concatenate((offset_array_vert, cropped_image3, cropped_image2), axis=1)

        # top, bottom 사이에 offset array를 제거하고 concatenate
        concat_image_all = np.concatenate((concat_image_top[:-3*offset_height,:,:], concat_image_bottom[3*offset_height:,:,:]), axis=0)

        # Thresholding
        concat_image_all_gray = cv2.cvtColor(concat_image_all, cv2.COLOR_RGB2GRAY)
        drone_image_thresh = cv2.adaptiveThreshold(concat_image_all_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)

        # Image show
        self.get_logger().info("Image window will be closed in 10 seconds")
        self.get_logger().info("Press any key to close the image window")
        cv2.imshow("2D map", drone_image_thresh)
        cv2.waitKey(10000)  # wait 10 seconds
        cv2.destroyAllWindows()

        # Map save
        self.get_logger().info("Map saving...")
        result = cv2.imwrite(self.workspace_path + self.map_file, drone_image_thresh)
    
        return self.map_file, result

    def write_yaml_file(self):
        yaml_content = f"""image: {self.map_file.split("/")[1]}
mode: trinary
resolution: 0.05
origin: [0, 0, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25"""

        yaml_file_descriptor = open(self.workspace_path + self.yaml_file, 'wt')
        yaml_file_descriptor.write(yaml_content)
        yaml_file_descriptor.close()


def main():
    rclpy.init()

    image_processor = ImageProcessor()

    rclpy.spin(image_processor)

    rclpy.shutdown()


if __name__ == "__main__":
    main()