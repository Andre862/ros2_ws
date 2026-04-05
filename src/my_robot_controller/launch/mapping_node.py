import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random
import math


class MappingNode(Node):
    def __init__(self):
        super().__init__('mapping_node')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Safer mapping speeds
        self.forward_speed = 0.15
        self.turn_speed = 0.6
        self.back_speed = -0.08

        # Distances from scan
        self.front_dist = 999.0
        self.left_dist = 999.0
        self.right_dist = 999.0

        # Simple state machine
        self.mode = "forward"
        self.mode_end_time = self.get_time() + random.uniform(2.0, 4.0)

        self.timer = self.create_timer(0.1, self.control_loop)

    def get_time(self):
        return self.get_clock().now().nanoseconds / 1e9

    def clean_min(self, values):
        clean = []
        for v in values:
            if v is None:
                continue
            if math.isinf(v) or math.isnan(v):
                continue
            clean.append(v)
        return min(clean) if clean else 999.0

    def scan_callback(self, msg):
        ranges = list(msg.ranges)
        n = len(ranges)
        if n == 0:
            return

        # Wider, more stable sectors
        front_sector = ranges[:15] + ranges[-15:]
        left_sector = ranges[n // 3 : n // 2]
        right_sector = ranges[n // 2 : 2 * n // 3]

        self.front_dist = self.clean_min(front_sector)
        self.left_dist = self.clean_min(left_sector)
        self.right_dist = self.clean_min(right_sector)

    def control_loop(self):
        twist = Twist()
        now = self.get_time()

        # Better thresholds for TurtleBot3 mapping
        front_close = self.front_dist < 0.60
        front_very_close = self.front_dist < 0.35
        left_close = self.left_dist < 0.45
        right_close = self.right_dist < 0.45

        # If something is right in front, stop backing and turn away
        if front_very_close:
            if self.left_dist > self.right_dist:
                self.mode = "turn_left"
            else:
                self.mode = "turn_right"
            self.mode_end_time = now + 1.2

        elif front_close:
            # Gentle recovery instead of random back-and-forth
            if self.mode != "back":
                self.mode = "back"
                self.mode_end_time = now + 0.6

        # Only change exploration mode when the current one expires
        elif now > self.mode_end_time:
            choices = ["forward", "forward", "forward", "turn_left", "turn_right"]
            self.mode = random.choice(choices)
            self.mode_end_time = now + random.uniform(1.5, 3.5)

        # Execute mode
        if self.mode == "forward":
            twist.linear.x = self.forward_speed

            # Gentle steering to stay centered in open areas
            if left_close and not right_close:
                twist.angular.z = -0.20
            elif right_close and not left_close:
                twist.angular.z = 0.20
            else:
                twist.angular.z = random.uniform(-0.08, 0.08)

        elif self.mode == "turn_left":
            twist.linear.x = 0.0
            twist.angular.z = self.turn_speed

        elif self.mode == "turn_right":
            twist.linear.x = 0.0
            twist.angular.z = -self.turn_speed

        elif self.mode == "back":
            twist.linear.x = self.back_speed
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = MappingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()