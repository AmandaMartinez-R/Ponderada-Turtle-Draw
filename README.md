# Visão Digital: Contornando uma Imagem com Turtle Draw


## Vídeo explicativo

Acesse o vídeo [aqui](https://youtu.be/8ULHrcfLp04)

## Visão geral

Este projeto combina **ROS 2**, **Turtlesim** e **processamento de imagem** para transformar uma imagem de entrada em um caminho de desenho e executar esse trajeto com uma tartaruga virtual.

O pacote principal está em `src/turtle_draw`, e o fluxo principal é:

1. Carregar a imagem `images/input/dog.png`.
2. Aplicar um pipeline de visão computacional para extrair contornos.
3. Converter os contornos em pontos de navegação compatíveis com o Turtlesim.
4. Executar o desenho por meio de um nó ROS 2.

## O que o projeto faz

- Gera uma trajetória a partir de uma imagem usando OpenCV.
- Controla a tartaruga no ambiente `turtlesim` via ROS 2.
- Disponibiliza três nós distintos:
  - `path_controller`: desenha a trajetória gerada a partir da imagem.
  - `point_controller`: navega até um ponto fixo.
  - `turtle_controller`: demonstra movimento contínuo da tartaruga.

## Requisitos

### Software

- ROS 2 (qualquer distro compatível com `rclpy` e o pacote `turtlesim`)
- Python 3
- `pip`
- `colcon`

### Dependências Python

Instale as dependências com:

```bash
python -m pip install -r requirements.txt
```

As dependências atuais são:

- `numpy`
- `opencv-python`
- `matplotlib`

### Dependências ROS 2

Você também precisa ter o ambiente ROS 2 configurado e o pacote `turtlesim` disponível, por exemplo:

```bash
source /opt/ros/<sua-distro>/setup.bash
```

## Estrutura de pastas

```text
Ponderada-Turtle-Draw/
├── build/                  # artefatos gerados pelo colcon
├── docs/                   # documentação complementar
├── images/
│   ├── input/
│   │   └── dog.png         # imagem usada pelo gerador de trajetória
│   └── output/             # imagens geradas / resultados
├── install/                # instalação do workspace
├── log/                    # logs de build
├── path_planning/          # utilitários e protótipos de planejamento
│   ├── __init__.py
│   └── coordinate_mapper.py
├── src/
│   └── turtle_draw/        # pacote ROS 2 principal
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       ├── resource/
│       ├── test/
│       └── turtle_draw/
│           ├── __init__.py
│           ├── path_controller.py
│           ├── point_controller.py
│           ├── turtle_controller.py
│           ├── utils/
│           │   ├── __init__.py
│           │   ├── path_generator.py
│           │   └── path_optimizer.py
│           └── vision/
│               ├── __init__.py
│               ├── blur.py
│               ├── closing.py
│               ├── contour_tracing.py
│               ├── contours.py
│               ├── convolution.py
│               ├── coordinate_conversion.py
│               ├── debug_pipeline.py
│               ├── dilation.py
│               ├── erosion.py
│               ├── filter_contours.py
│               ├── grayscale.py
│               ├── invert.py
│               ├── outer_contour.py
│               ├── path_smoothing.py
│               ├── sobel.py
│               ├── threshold.py
│               └── visualization.py
└── README.md
```

## Como funciona o pipeline

O arquivo `src/turtle_draw/turtle_draw/utils/path_generator.py` executa o fluxo abaixo:

1. Carrega a imagem `images/input/dog.png`.
2. Converte para tons de cinza.
3. Aplica blur para reduzir ruído.
4. Detecta bordas com Sobel.
5. Realiza thresholding.
6. Extrai contornos.
7. Filtra contornos pequenos.
8. Converte os pontos para o sistema de coordenadas usado pelo Turtlesim.

Esse pipeline gera uma sequência de pontos usada pelo `path_controller` para movimentar a tartaruga.

## Como usar

### 1. Preparar o ambiente

```bash
cd Ponderada-Turtle-Draw
source /opt/ros/<sua-distro>/setup.bash
python -m pip install -r requirements.txt
```

### 2. Construir o pacote

```bash
colcon build --packages-select turtle_draw
source install/setup.bash
```

### 3. Iniciar o `turtlesim`

```bash
ros2 run turtlesim turtlesim_node
```

### 4. Executar os nós

#### a) Desenhar a trajetória da imagem

```bash
ros2 run turtle_draw path_controller
```

Esse nó vai desenhar a trajetória gerada pela imagem `images/input/dog.png`.

#### b) Ir para um ponto fixo

```bash
ros2 run turtle_draw point_controller
```

Esse nó leva a tartaruga até o ponto `(8, 8)`.

#### c) Movimentação básica de demonstração

```bash
ros2 run turtle_draw turtle_controller
```

Esse nó aplica um movimento constante e serve como exemplo de integração com o `cmd_vel`.

## Fluxo recomendado para teste

```bash
# Terminal 1
cd Ponderada-Turtle-Draw
source /opt/ros/<sua-distro>/setup.bash
source install/setup.bash
ros2 run turtlesim turtlesim_node

# Terminal 2
cd Ponderada-Turtle-Draw
source /opt/ros/<sua-distro>/setup.bash
source install/setup.bash
ros2 run turtle_draw path_controller
```

## Arquivos e módulos principais

### `src/turtle_draw/turtle_draw/path_controller.py`

- Torna-se o nó principal para o desenho.
- Publica em `/turtle1/cmd_vel`.
- Se inscreve em `/turtle1/pose`.
- Usa `SetPen` para habilitar a caneta.
- Controla o avanço ponto a ponto até o fim da trajetória.

### `src/turtle_draw/turtle_draw/point_controller.py`

- Controla a tartaruga até um ponto definido.
- Útil para testes de navegação e validação de controle.

### `src/turtle_draw/turtle_draw/turtle_controller.py`

- Exemplo de controlador simples.
- Move a tartaruga em loop com velocidades constantes.

### `src/turtle_draw/turtle_draw/utils/path_generator.py`

- Faz a geração automática da trajetória a partir da imagem.
- É o ponto de integração entre visão computacional e controle ROS.

### `src/turtle_draw/turtle_draw/vision/`

- Contém os módulos do pipeline de processamento de imagem.
- Cada arquivo é responsável por uma etapa do fluxo de extração de contorno.

## Como personalizar o projeto

### Trocar a imagem de entrada

A imagem usada atualmente é `images/input/dog.png`. Para trocar, altere o caminho em `path_generator.py` ou substitua o arquivo mantendo o mesmo nome.

### Ajustar o comportamento do desenho

Você pode ajustar parâmetros em:

- `path_controller.py`: tolerância de chegada (`distance < 0.15`), ganhos angulares e lineares.
- `path_generator.py`: threshold, filtro de contornos e amostragem de pontos.
- `vision/*`: parâmetros de blur, erosão, dilatação e filtragem.

## Testes e qualidade

O pacote inclui testes de formato e copyright em `src/turtle_draw/test/`.

Para validar a instalação do pacote, rode:

```bash
colcon test --packages-select turtle_draw
colcon test-result --verbose
```

## Problemas comuns e solução

### `ModuleNotFoundError` para `rclpy`

- Certifique-se de que o ambiente ROS 2 foi carregado com `source /opt/ros/<sua-distro>/setup.bash`.

### `Imagem não encontrada`

- Verifique se `images/input/dog.png` existe.
- Confirme se o caminho em `path_generator.py` aponta para a raiz correta do projeto.

### `set_pen` não responde

- Verifique se o `turtlesim` está rodando.
- Confirme se o nó está publicando em `/turtle1/cmd_vel`.

### Erro de build

- Rode `colcon build --packages-select turtle_draw` novamente.
- Garanta que o ambiente ROS foi sourced antes de executar o build.

## Observações adicionais

- Os diretórios `build/`, `install/` e `log/` são gerados automaticamente e não devem ser editados manualmente.
- O diretório `path_planning/` contém utilitários e experimentos auxiliares e pode ser usado como ponto de extensão para novas estratégias de planejamento.
- O pacote principal está em `src/turtle_draw`, então a maioria do desenvolvimento acontece lá.

## Contribuição

Se quiser evoluir o projeto, os pontos mais promissores são:

- Melhorar o pipeline de visão para tratar imagens mais complexas.
- Adicionar visualização do caminho antes do desenho.
- Implementar comandos ROS 2 de launch para automatizar a execução.
- Melhorar a documentação e a parametrização dos controladores.

## Resumo

Este repositório oferece um fluxo completo de **processamento de imagem + controle de tartaruga via ROS 2**, com um pacote ROS 2 organizado em `src/turtle_draw`. O caminho principal para executar a demonstração é:

1. `source /opt/ros/<sua-distro>/setup.bash`
2. `colcon build --packages-select turtle_draw`
3. `source install/setup.bash`
4. `ros2 run turtlesim turtlesim_node`
5. `ros2 run turtle_draw path_controller`
