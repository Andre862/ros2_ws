#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class TurtlebotMapper(Node):
    def __init__(self):
        super().__init__("turtlebot_mapper")
        self.get_logger().info("Turtlebot Mapper started.")

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_sub = self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)

        self.last_turn = 1  # 1 = left, -1 = right

        # Tuning
        self.forward_speed = 0.16
        self.slow_speed = 0.06
        self.turn_speed = 0.45
        self.stop_distance = 0.55
        self.slow_distance = 0.90
        self.side_distance = 0.40

        self.scan = None

    def scan_callback(self, scan: LaserScan):
        self.scan = scan
        cmd = Twist()

        front = self.sector_min(scan, -0.25, 0.25)
        left = self.sector_min(scan, 0.80, 1.60)
        right = self.sector_min(scan, -1.60, -0.80)
        front_left = self.sector_min(scan, 0.20, 0.80)
        front_right = self.sector_min(scan, -0.80, -0.20)

        if not math.isfinite(front):
            front = 10.0
        if not math.isfinite(left):
            left = 10.0
        if not math.isfinite(right):
            right = 10.0
        if not math.isfinite(front_left):
            front_left = 10.0
        if not math.isfinite(front_right):
            front_right = 10.0

        # Too close in front: turn toward the more open side
        if front < self.stop_distance:
            self.last_turn = 1 if left > right else -1
            cmd.linear.x = 0.03
            cmd.angular.z = self.last_turn * self.turn_speed

        # Close to obstacle: slow down and bias away from the nearest side
        elif front < self.slow_distance:
            cmd.linear.x = self.slow_speed
            if front_left < front_right:
                cmd.angular.z = -0.25
            else:
                cmd.angular.z = 0.25

        # Side too close: steer away from it
        elif left < self.side_distance:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = -0.25
        elif right < self.side_distance:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.25

        # Clear path: go forward
        else:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

    def sector_min(self, scan: LaserScan, ang_min: float, ang_max: float) -> float:
        best = float("inf")

        for i, d in enumerate(scan.ranges):
            angle = scan.angle_min + i * scan.angle_increment
            if ang_min <= angle <= ang_max:
                if math.isfinite(d) and scan.range_min < d < scan.range_max:
                    if d < best:
                        best = d

        return best


def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()