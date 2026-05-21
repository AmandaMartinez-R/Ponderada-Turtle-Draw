import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist


class TurtleController(Node):

    def __init__(self):

        # Nome do nó
        super().__init__('turtle_controller')

        # Cria publisher
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Timer
        timer_period = 0.1

        self.timer = self.create_timer(
            timer_period,
            self.move_turtle
        )

        self.get_logger().info(
            'Turtle Controller iniciado!'
        )

    def move_turtle(self):

        # Cria mensagem
        msg = Twist()

        # Movimento linear
        msg.linear.x = 2.0

        # Rotação
        msg.angular.z = 1.0

        # Publica mensagem
        self.publisher_.publish(msg)

        self.get_logger().info(
            'Movendo tartaruga...'
        )


def main(args=None):

    # Inicializa ROS
    rclpy.init(args=args)

    # Cria nó
    node = TurtleController()

    # Mantém nó ativo
    rclpy.spin(node)

    # Finaliza
    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()