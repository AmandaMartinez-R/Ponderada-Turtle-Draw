import math

import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose


class PointController(Node):

    def __init__(self):

        super().__init__('point_controller')

        # Publisher
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Subscriber
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Timer
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        # Pose atual
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Objetivo
        self.goal_x = 8.0
        self.goal_y = 8.0

        self.get_logger().info(
            'Point Controller iniciado!'
        )

    def pose_callback(self, msg):

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def control_loop(self):

        # Calcula diferença
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y

        # Distância até objetivo
        distance = math.sqrt(
            dx**2 + dy**2
        )

        # Ângulo desejado
        target_angle = math.atan2(
            dy,
            dx
        )

        # Erro angular
        angle_error = (
            target_angle
            - self.current_theta
        )

        # Mensagem
        msg = Twist()

        # Controle angular
        msg.angular.z = 4.0 * angle_error

        # Controle linear
        msg.linear.x = 2.0 * distance

        # Limita velocidade
        if msg.linear.x > 2.0:
            msg.linear.x = 2.0

        # Se chegou perto
        if distance < 0.1:

            msg.linear.x = 0.0
            msg.angular.z = 0.0

            self.get_logger().info(
                'Objetivo alcançado!'
            )

        # Publica
        self.publisher_.publish(msg)

   


def main(args=None):

    rclpy.init(args=args)

    node = PointController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()