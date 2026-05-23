import math

import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

from turtlesim.srv import SetPen

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

        # Serviço da caneta
        self.set_pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        while not self.set_pen_client.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info(
                'Aguardando serviço set_pen...'
            )

        # Pose atual
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        self.pose_received = False

        # Gera trajetória
        self.path = generate_drawing_path()

        # Índice do ponto atual
        self.current_point_index = 0

        # Inicialização da caneta
        self.pen_initialized = False

        # Timer principal
        self.timer = self.create_timer(
            0.05,
            self.control_loop
        )

        self.get_logger().info(
            f'Trajetória carregada com '
            f'{len(self.path)} pontos.'
        )

    def set_pen(self, off):

        request = SetPen.Request()

        request.r = 255
        request.g = 255
        request.b = 255

        request.width = 2

        request.off = 1 if off else 0

        self.set_pen_client.call_async(request)

    def pose_callback(self, msg):

        """
        Atualiza posição atual.
        """

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

        self.pose_received = True

    def control_loop(self):

        """
        Controle principal.
        """

        if not self.pose_received:
            return

        # Inicializa caneta
        if not self.pen_initialized:

            self.set_pen(off=False)

            self.pen_initialized = True

            return

        # Verifica fim
        if self.current_point_index >= len(self.path):

            stop_msg = Twist()

            self.publisher_.publish(stop_msg)

            self.get_logger().info(
                'Desenho finalizado!'
            )

            return

        # Obtém ponto alvo
        goal_x, goal_y = self.path[
            self.current_point_index
        ]

        # Diferenças
        dx = goal_x - self.current_x
        dy = goal_y - self.current_y

        # Distância correta
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

        # Cria comando
        msg = Twist()

        # Controle angular
        msg.angular.z = 4.0 * angle_error

        # Controle linear
        msg.linear.x = 1.5 * distance

        # Limite
        if msg.linear.x > 2.0:
            msg.linear.x = 2.0

        # Se desalinhado:
        # gira primeiro
        if abs(angle_error) > 0.3:

            msg.linear.x = 0.0

        # Chegou no ponto
        if distance < 0.15:

            self.current_point_index += 1

            self.get_logger().info(
                f'Ponto alcançado: '
                f'{self.current_point_index}'
            )

        # Publica movimento
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