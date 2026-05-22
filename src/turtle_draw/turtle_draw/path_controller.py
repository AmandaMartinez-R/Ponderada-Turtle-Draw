import math

import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose


class PathController(Node):

    def __init__(self):

        super().__init__('path_controller')

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

        # Lista de pontos
        self.path = [

            (2.0, 2.0),
            (8.0, 2.0),
            (8.0, 8.0),
            (2.0, 8.0),
            (2.0, 2.0)

        ]

        # Índice atual
        self.current_goal_index = 0

        self.get_logger().info(
            'Path Controller iniciado!'
        )

    def pose_callback(self, msg):

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def control_loop(self):

        # Se terminou todos os pontos
        if self.current_goal_index >= len(self.path):

            stop_msg = Twist()

            self.publisher_.publish(stop_msg)

            self.get_logger().info(
                'Desenho finalizado!'
            )

            return

        # Objetivo atual
        goal_x, goal_y = self.path[
            self.current_goal_index
        ]

        # Diferença
        dx = goal_x - self.current_x
        dy = goal_y - self.current_y

        # Distância
        distance = math.sqrt(
            dx**2 + dy**2
        )

        # Ângulo alvo
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

        # Limite velocidade
        if msg.linear.x > 2.0:
            msg.linear.x = 2.0

        # Chegou no ponto?
        if distance < 0.2:

            self.get_logger().info(
                f'Ponto alcançado: '
                f'{self.current_goal_index}'
            )

            # Próximo ponto
            self.current_goal_index += 1

        # Publica
        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = PathController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()