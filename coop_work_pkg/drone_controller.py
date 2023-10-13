import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleStatus
from px4_msgs.msg import VehicleCommand


class DroneController(Node):

    def __init__(self):
        super().__init__('drone_controller')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.vehicle_status_sub_ = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status',
            self.vehicle_status_callback,
            qos_profile)
        self.keyboard_input_sub_ = self.create_subscription(
            Twist,
            '/keyboard_input',
            self.keyboard_input_callback,
            QoSProfile(depth=10))
        self.gimbal_input_sub_ = self.create_subscription(
            Vector3,
            '/gimbal_input',
            self.gimbal_input_callback,
            QoSProfile(depth=10))
        self.offboard_control_mode_publisher_ = self.create_publisher(
            OffboardControlMode,
            '/fmu/in/offboard_control_mode',
            qos_profile)
        self.vehicle_command_publisher_ = self.create_publisher(
            VehicleCommand,
            '/fmu/in/vehicle_command',
            qos_profile)
        self.trajectory_setpoint_publisher_ = self.create_publisher(
            TrajectorySetpoint,
            '/fmu/in/trajectory_setpoint',
            qos_profile)
        self.timer_period = 0.02  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX
        self.counter = 0
        # vehicle coordinate. (NED|Y, m|deg)
        self.north = 0.0
        self.east = 0.0
        self.down = -5.0
        self.yaw = 0.0
        # gimbal orientation. (angle, [-180,180]degree)
        self.gimbal_roll = 0.0
        self.gimbal_pitch = 0.0
        self.gimbal_yaw = 0.0

        self.landing = False

    def vehicle_status_callback(self, msg):
        if self.nav_state != VehicleStatus.NAVIGATION_STATE_OFFBOARD:
            print("NAV_STATUS: ", msg.nav_state)
            print("  - offboard status: ", VehicleStatus.NAVIGATION_STATE_OFFBOARD)
        self.nav_state = msg.nav_state

    def keyboard_input_callback(self, msg):
        # /keyboard_input topic을 받아서 적용
        self.north = msg.linear.x
        self.east = msg.linear.y
        self.down = msg.linear.z
        self.yaw = msg.angular.z
        if self.down == 0:
            self.landing = True

        print(f"NED|Y: {self.north}, {self.east}, {self.down} | {self.yaw}")

    def gimbal_input_callback(self, msg):
        # /gimbal_input topic을 받아서 적용
        self.gimbal_roll = msg.x
        self.gimbal_pitch = msg.y
        self.gimbal_yaw = msg.z

        print(f"RPY: {self.gimbal_roll}, {self.gimbal_pitch}, {self.gimbal_yaw}")
        self.publish_gimbal_setpoint_py(self.gimbal_pitch, self.gimbal_yaw)

    def timer_callback(self):
        if self.counter == int(1 / self.timer_period):  # after 1 second
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.arm()
            self.publish_gimbal_config()

        self.publish_offboard_control_mode()    # offboard control을 얻기 위해 2Hz 이상으로 계속 publish해야 함
        if self.landing:
            self.land()  # 착륙
            self.landing = False    # 반복적 land() 호출을 막기 위함
        else:
            self.publish_trajectory_setpoint(
                self.north,
                self.east,
                self.down,
                self.yaw)  # world 좌표 (NED 좌표계)

        if self.counter < int(1 / self.timer_period) + 1:
            self.counter += 1

    def publish_vehicle_command(
            self,
            command,
            param1,
            param2,
            param3=0.0,
            param4=0.0,
            param5=0.0,
            param6=0.0,
            param7=0.0):
        vehicle_command_msg = VehicleCommand()
        vehicle_command_msg.param1 = param1
        vehicle_command_msg.param2 = param2
        vehicle_command_msg.param3 = param3
        vehicle_command_msg.param4 = param4
        vehicle_command_msg.param5 = param5
        vehicle_command_msg.param6 = param6
        vehicle_command_msg.param7 = param7
        vehicle_command_msg.command = command
        vehicle_command_msg.target_system = 1
        vehicle_command_msg.target_component = 1
        vehicle_command_msg.source_system = 1
        vehicle_command_msg.source_component = 1
        vehicle_command_msg.from_external = True
        vehicle_command_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        self.vehicle_command_publisher_.publish(vehicle_command_msg)

    def publish_offboard_control_mode(self):
        # Publish offboard control modes
        offboard_msg = OffboardControlMode()
        offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        offboard_msg.position = True
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        self.offboard_control_mode_publisher_.publish(offboard_msg)

    def publish_trajectory_setpoint(self, north, east, down, yaw):
        trajectory_msg = TrajectorySetpoint()   # world 좌표 (NED frame)
        trajectory_msg.position[0] = north
        trajectory_msg.position[1] = east
        trajectory_msg.position[2] = down
        trajectory_msg.yaw = yaw * 3.14 / 180  # rad
        trajectory_msg.yawspeed = 0.52  # 0.52 rad/s = 30 deg/s
        self.trajectory_setpoint_publisher_.publish(trajectory_msg)

    def publish_gimbal_setpoint_py(self, pitch, yaw):
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_DO_GIMBAL_MANAGER_PITCHYAW,
            pitch,
            yaw,
            float("nan"),
            float("nan"),
            param5=12.0)  # pitch/yaw rate = NaN, flag = 12

        self.get_logger().info(f"Gimbal setpoint sent (pitch={pitch}, yaw={yaw})")

    def publish_gimbal_config(self):
        # Publish gimbal configuration for offboard control
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_DO_GIMBAL_MANAGER_CONFIGURE,
            1.0,
            1.0)  # primary sysid/compid=1.0/1.0

        self.get_logger().info("Gimbal configuration sent")

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0, 0.0)

        self.get_logger().info("Arm command sent")

    def land(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, 0.0, 0.0)

        self.get_logger().info("Land command sent")


def main(args=None):
    rclpy.init(args=args)

    drone_controller = DroneController()

    rclpy.spin(drone_controller)

    drone_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
