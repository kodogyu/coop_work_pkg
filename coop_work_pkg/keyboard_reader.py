import rclpy

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

from std_msgs.msg import Char

msg = """
Keyboard Reader for Drone controller Activated
----------------------------------------------
Available Keys:
    w       r       i
a   s   d
    x               m

w/x : +/-1(m) North coordinate of the drone
d/a : +/-1(m) East coordinate of the drone
m/i : +/-1(m) Down coordinate of the drone
s   : Move to (0, 0, D)
r   : Return to the Starting point

CTRL-C to quit
"""

def main():
    rclpy.init()

    qos_profile = QoSProfile(depth=10)
    node = rclpy.create_node('keyboard_reader')
    keyboard_input_publisher = node.create_publisher(Char, '/keyboard_input', qos_profile)

    stack = 0
    north = 0.0
    east = 0.0
    down = -5.0

    print(msg)
    while(1):
        key = input("direction: ")
        if key == 'w':
            north += 1
            stack += 1
        elif key == 'x':
            north -= 1
            stack += 1
        elif key == 'a':
            east -= 1
            stack += 1
        elif key == 'd':
            east += 1
            stack += 1
        elif key == 'i':
            down += 1
            stack += 1
        elif key == 'm':
            down -= 1
            stack += 1
        elif key == 's':
            north = 0.0
            east = 0.0
            stack += 1
        elif key == 'r':
            north = 0.0
            east = 0.0
            down = -5.0
            stack += 1
        else:
            if (key == '\x03'):
                break
        print(f"NED: {north}, {east}, {down}")

        keyboard_msg = Char()
        keyboard_msg.data = ord(key)

        keyboard_input_publisher.publish(keyboard_msg)  # Todo : message type geometry_msgs.msg.Point로 바꾸기

        if stack == 20:
            print(msg)
            stack = 0

if __name__ == '__main__':
    main()