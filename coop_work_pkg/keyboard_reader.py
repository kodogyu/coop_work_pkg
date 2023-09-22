import rclpy

from rclpy.qos import QoSProfile

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

msg = """
Keyboard Reader for Drone controller Activated
----------------------------------------------
Available Keys:
q   w   e   r   t       i
a   s   d       g   h           l
    x           v       m

w/x : +/-1(m) North coordinate of the drone
d/a : +/-1(m) East coordinate of the drone
m/i : +/-1(m) Down coordinate of the drone
e/q : +/-90(deg) yaw of the drone
s   : Move to (0, 0, D)
r   : Return to the Starting point
l   : Land

t/v : +/-90(degree) Gimbal pitch
h/g : +/-90(degree) Gimbal yaw

CTRL-C to quit
"""

def main():
    rclpy.init()

    qos_profile = QoSProfile(depth=10)
    node = rclpy.create_node('keyboard_reader')
    keyboard_input_publisher = node.create_publisher(Twist, '/keyboard_input', qos_profile)
    gimbal_input_publisher = node.create_publisher(Vector3, '/gimbal_input', qos_profile)

    stack = 0

    # Vehicle position
    north = 0.0
    east = 0.0
    down = -5.0
    yaw = 0.0

    # Gimbal orientation
    gimbal_roll = 0.0
    gimbal_pitch = 0.0
    gimbal_yaw = 0.0

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
        elif key == 'e':    # 10도 회전 (CW)
            yaw += 10
        elif key == 'q':    # -10도 회전 (CCW)
            yaw -= 10
        # gimbal keys
        elif key == 't':    # head up
            gimbal_pitch += 90
        elif key == 'v':    # head down
            gimbal_pitch -= 90
        elif key == 'h':
            gimbal_yaw += 90
        elif key == "g":
            gimbal_yaw -= 90
        else:
            if (key == '\x03'):
                break
        stack += 1
        print(f"NED|Y: {north}, {east}, {down} | {yaw}")
        print(f"RPY: {gimbal_roll}, {gimbal_pitch}, {gimbal_yaw}")

        if gimbal_pitch < -180 or gimbal_pitch > 180 or gimbal_yaw < -180 or gimbal_yaw > 180:
            print("pitch, yaw should be in range [-180, 180]. Returning to (pitch=0, yaw=0).")
            gimbal_pitch = 0.0
            gimbal_yaw = 0.0
        

        # publish Keyboard input
        keyboard_msg = Twist()  # (x, y, z | x, y, z) = (north, east, down | roll, pitch, yaw)
        keyboard_msg.linear.x = north
        keyboard_msg.linear.y = east
        keyboard_msg.linear.z = down
        keyboard_msg.angular.z = yaw
        keyboard_input_publisher.publish(keyboard_msg)

        # publish Gimbal input
        gimbal_msg = Vector3()    # (x, y, z) = (roll, pitch, yaw)
        gimbal_msg.x = gimbal_roll
        gimbal_msg.y = gimbal_pitch
        gimbal_msg.z = gimbal_yaw
        gimbal_input_publisher.publish(gimbal_msg)

        if stack == 20:
            print(msg)
            stack = 0

if __name__ == '__main__':
    main()