import rclpy

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

# from std_msgs.msg import Char
from geometry_msgs.msg import Point

msg = """
Keyboard Reader for Drone controller Activated
----------------------------------------------
Available Keys:
    w       r       i
a   s   d                   l
    x               m

w/x : +/-1(m) North coordinate of the drone
d/a : +/-1(m) East coordinate of the drone
m/i : +/-1(m) Down coordinate of the drone
s   : Move to (0, 0, D)
r   : Return to the Starting point
l   : Land

CTRL-C to quit
"""

def main():
    rclpy.init()

    qos_profile = QoSProfile(depth=10)
    node = rclpy.create_node('keyboard_reader')
    keyboard_input_publisher = node.create_publisher(Point, '/keyboard_input', qos_profile)

    stack = 0
    north = 0.0
    east = 0.0
    down = -5.0

    print(msg)
    while(1):
        key = input("direction: ")
        if key == 'w':
            north += 1
        elif key == 'x':
            north -= 1
        elif key == 'a':
            east -= 1
        elif key == 'd':
            east += 1
        elif key == 'i':    # 상승
            down -= 1
        elif key == 'm':    # 하강
            down += 1
        elif key == 's':    # 원점으로 이동
            north = 0.0
            east = 0.0
            stack += 1
        elif key == 'r':    # 귀환
            north = 0.0
            east = 0.0
            down = -5.0
        elif key == 'l':
            down = 0.0
        else:
            if (key == '\x03'):
                break
        stack += 1
        print(f"NED: {north}, {east}, {down}")

        # keyboard_msg = Char()
        # keyboard_msg.data = ord(key)
        # keyboard_input_publisher.publish(keyboard_msg)

        keyboard_msg = Point()  # (x, y, z) = (north, east, down)
        keyboard_msg.x = north
        keyboard_msg.y = east
        keyboard_msg.z = down
        keyboard_input_publisher.publish(keyboard_msg)

        if stack == 20:
            print(msg)
            stack = 0

if __name__ == '__main__':
    main()