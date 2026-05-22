import math

import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

# Importa gerador de trajetória
from turtle_draw.utils.path_generator import (
    generate_drawing_path
)


class PathController(Node):

    def __init__(self):

        # Inicializa nó
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

        # Timer de controle
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        # Pose atual
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Gera trajetória da imagem
        self.path = generate_drawing_path()

        # Índice do waypoint atual
        self.current_goal_index = 0

        self.get_logger().info(
            f'Trajetória carregada com '
            f'{len(self.path)} pontos.'
        )

    def pose_callback(self, msg):

        """
        Atualiza posição atual da tartaruga.
        """

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def control_loop(self):

        """
        Loop principal de controle.
        """

        # Verifica se terminou
        if self.current_goal_index >= len(self.path):

            stop_msg = Twist()

            self.publisher_.publish(stop_msg)

            self.get_logger().info(
                'Desenho finalizado!'
            )

            return

        # Obtém waypoint atual
        goal_x, goal_y = self.path[
            self.current_goal_index
        ]

        # Diferença
        dx = goal_x - self.current_x
        dy = goal_y - self.current_y

        # Distância euclidiana
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

        # Normaliza ângulo
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        # Cria mensagem
        msg = Twist()

        # Controle angular
        msg.angular.z = 4.0 * angle_error

        # Controle linear
        msg.linear.x = 2.0 * distance

        # Limita velocidade linear
        if msg.linear.x > 2.0:
            msg.linear.x = 2.0

        # Se estiver muito desalinhado:
        # gira antes de andar
        if abs(angle_error) > 0.5:

            msg.linear.x = 0.0

        # Verifica chegada
        if distance < 0.2:

            self.get_logger().info(
                f'Ponto alcançado: '
                f'{self.current_goal_index}'
            )

            self.current_goal_index += 1

        # Publica comando
        self.publisher_.publish(msg)


def main(args=None):

    # Inicializa ROS
    rclpy.init(args=args)

    # Cria nó
    node = PathController()

    # Mantém execução
    rclpy.spin(node)

    # Finaliza
    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()