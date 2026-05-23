# Relatório Técnico - Turtle Draw com ROS 2


## 1. Resumo Executivo

Este projeto teve como objetivo transformar uma imagem em uma trajetória desenhável pela tartaruga do simulador `turtlesim`, usando ROS 2 como infraestrutura de controle e um pipeline de visão computacional implementado manualmente.

Ao longo do desenvolvimento, a solução evoluiu de uma abordagem experimental para um pacote ROS 2 organizado, com separação entre processamento de imagem, conversão de coordenadas e controle do robô. O resultado mais relevante foi a criação de um fluxo funcional de geração de caminho e execução do movimento, embora o desenho completo do cachorro ainda não tenha sido concluído.

> Breve observação: o cachorro não foi desenhado integralmente; o sistema conseguiu gerar e seguir parte da trajetória, mas ainda há limitação na extração/seleção do contorno suficiente para fechar o desenho completo.

---

## 2. Objetivo do Projeto

O projeto buscou demonstrar a integração entre:

1. **processamento de imagem**;
2. **representação geométrica de contornos**;
3. **controle de robôs em ROS 2**;
4. **execução em ambiente simulado**.

A implementação foi feita com foco em aprendizado prático dos conceitos de visão computacional e controle, sem depender de bibliotecas prontas de segmentação ou rastreamento de contornos.

### Tecnologias utilizadas

- **ROS 2** para comunicação entre nós e publicação em tópicos;
- **Python** para a lógica de processamento e controle;
- **NumPy** para operações matriciais e convolução;
- **OpenCV** apenas para leitura da imagem;
- **Matplotlib** apenas para visualização auxiliar.

---

## 3. Arquitetura do Projeto

A arquitetura foi organizada em dois blocos principais:

### 3.1 Pipeline de visão computacional

Responsável por transformar a imagem original em um conjunto de pontos representando o contorno da figura.

### 3.2 Controle robótico ROS 2

Responsável por receber a trajetória gerada e converter essa informação em comandos de movimento para a tartaruga.

### 3.3 Estrutura do pacote

O pacote principal encontra-se em `src/turtle_draw`, com os seguintes componentes relevantes:

- `path_controller.py`: nó principal para desenhar a trajetória gerada;
- `point_controller.py`: nó auxiliar para navegação até um ponto fixo;
- `turtle_controller.py`: nó de demonstração com movimento controlado;
- `utils/path_generator.py`: ponto de integração entre visão computacional e ROS;
- `vision/`: módulos dedicados às etapas do pipeline de imagem;
- `setup.py`: definição dos nós executáveis do pacote.

Essa separação permitiu isolar etapas do desenvolvimento e facilitar testes parciais.

---

## 4. Desenvolvimento do Pipeline de Imagem

### 4.1 Leitura da imagem

A imagem utilizada como entrada é `images/input/dog.png`. Ela foi carregada com OpenCV e posteriormente tratada internamente pelo pacote.

### 4.2 Conversão para escala de cinza

A etapa de grayscale foi implementada manualmente usando a fórmula:

```math
Gray = 0.299R + 0.587G + 0.114B
```

Essa etapa reduziu a complexidade da informação e simplificou a segmentação posterior.

### 4.3 Suavização

O blur foi implementado por convolução manual com kernels em NumPy. Essa etapa serviu para reduzir ruído e suavizar pequenas variações de intensidade que atrapalhavam a extração dos contornos.

### 4.4 Sobel

O operador Sobel foi aplicado manualmente para destacar transições de intensidade e obter um mapa de bordas útil para o restante do processamento.

### 4.5 Threshold

A etapa de threshold foi implementada manualmente. O objetivo foi separar a região de interesse do fundo da imagem, transformando os pixels relevantes em branco e o restante em preto.

### 4.6 Extração e filtragem de contornos

A detecção de contornos foi feita manualmente no módulo `contours.py`, com:

- detecção de componentes conectados;
- ordenação dos pontos do contorno;
- filtragem de contornos pequenos em `filter_contours.py`.

Esse filtro foi importante para eliminar partes espúrias que geravam trajetórias irreais.

### 4.7 Conversão para coordenadas do turtlesim

A conversão de pixels para o espaço do `turtlesim` foi feita em `coordinate_conversion.py`, com normalização e inversão do eixo Y para se adaptar ao sistema de coordenadas do simulador.

### 4.8 Amostragem da trajetória

A trajetória final foi gerada a partir dos pontos convertidos e submetida a amostragem para reduzir o número excessivo de pontos, evitando movimentos excessivamente densos e instáveis.

---

## 5. Controle da Tartaruga no ROS 2

O controle da tartaruga foi implementado em um nó ROS 2, com o comportamento principal concentrado em `path_controller.py`.

### 5.1 Funções principais do controlador

O nó faz uso de:

- `Pose` para monitorar a posição atual da tartaruga;
- `Twist` para publicar comandos de velocidade;
- `SetPen` para ligar a caneta e registrar o desenho.

### 5.2 Estratégia de controle

A lógica de movimentação utiliza um controle proporcional simples:

- **velocidade angular** proporcional ao erro angular;
- **velocidade linear** proporcional à distância até o ponto-alvo;
- **limite máximo** para evitar comandos agressivos.

Quando a tartaruga fica alinhada com o próximo ponto, o controlador passa a avançar; quando o alvo é alcançado, o índice do ponto atual é incrementado.

### 5.3 Nós auxiliares

Além de `path_controller.py`, o pacote também contém:

- `point_controller.py`, utilizado para testar navegação até um objetivo fixo;
- `turtle_controller.py`, utilizado como demonstração de movimento básico.

---

## 6. Principais Dificuldades e Como Foram Superadas

### 6.1 Configuração do ambiente ROS 2

A configuração inicial do ambiente foi um ponto de atrito por conta de dependências e do fluxo de build do workspace. O projeto tornou-se estável após a organização correta do pacote e a definição clara dos nós expostos em `setup.py`.

### 6.2 Organização dos imports e estrutura do pacote

Durante a integração, houve problemas de importação entre módulos internos do pacote. A solução foi padronizar a estrutura em `src/turtle_draw/turtle_draw` e garantir que os módulos fossem importados de forma consistente.

### 6.3 Geração de contornos válidos

A maior dificuldade técnica foi transformar a imagem em uma trajetória desenhável. Muitos testes mostraram que contornos incompletos e trajetórias excessivas causavam comportamento incorreto.

Para resolver isso:

- o pipeline foi ajustado para reduzir ruído;
- contornos pequenos foram filtrados;
- a trajetória foi amostrada;
- a conversão para coordenadas do `turtlesim` foi refinada.

### 6.4 Ajuste do comportamento da tartaruga

A tartaruga apresentava oscilações e rotações excessivas quando os ganhos de controle eram altos. O ajuste fino de velocidade e tolerância de chegada foi essencial para estabilizar o movimento.

### 6.5 Limitação do desenho completo do cachorro

Apesar do avanço no pipeline, o desenho não ficou completamente fiel ao cachorro. A trajetória gerada ainda ficou parcial, o que indica que a segmentação e a conversão dos contornos precisam ser refinadas para melhorar a continuidade e a cobertura da silhueta.

---

## 7. Resultados Obtidos

### 7.1 O que funcionou

- Leitura e processamento da imagem de entrada;
- Implementação manual do pipeline de visão computacional;
- Conversão da imagem em pontos navegáveis;
- Integração com o ROS 2 e publicação de comandos em `/turtle1/cmd_vel`;
- Funcionamento dos nós `path_controller`, `point_controller` e `turtle_controller`;
- Organização do projeto em um pacote ROS 2 reutilizável.

### 7.2 O que ainda limita o projeto

- O contorno extraído ainda não representa todo o cachorro de forma completa;
- a trajetória precisa ser refinada para reduzir lacunas e trechos desconexos;
- a experiência atual depende fortemente da parametrização do pipeline e dos ganhos do controlador.

---

## 8. Impacto do Projeto

O projeto foi relevante como exercício prático de integração entre visão computacional e robótica. Ele permitiu consolidar conceitos como:

- convolução manual;
- thresholding;
- detecção de contornos;
- mapeamento de coordenadas;
- comunicação em ROS 2;
- controle proporcional de movimento;
- organização de um pacote ROS 2.

Além disso, o projeto mostrou de forma concreta como um sistema visual pode ser conectado a um robô simulado para transformar uma imagem em um comportamento físico no ambiente do `turtlesim`.

---

## 9. Conclusão

O projeto atingiu o objetivo de construir uma solução funcional de **desenho por trajetória**, com integração entre visão computacional e ROS 2. A implementação foi conduzida de maneira modular, com foco em aprendizado técnico e organização do código.

A principal limitação observada foi a **incompletude do desenho do cachorro**, que ocorre pela dificuldade em obter um contorno contínuo e consistente a partir da imagem original. Ainda assim, o trabalho consolida uma base sólida para melhorias futuras, como:

- aprimorar o pipeline de segmentação;
- melhorar o rastreamento e a continuidade do contorno;
- adicionar visualização prévia da trajetória;
- parametrizar os controladores por arquivo de configuração;
- automatizar a execução com launch files do ROS 2.

---

## 10. Próximos Passos Recomendados

1. Refinar o algoritmo de extração de contorno para melhorar a fidelidade do desenho.
2. Avaliar a possibilidade de suavizar e interpolar a trajetória gerada.
3. Adicionar uma etapa de visualização da trajetória antes da execução.
4. Automatizar a execução do fluxo completo com arquivos `launch`.
5. Documentar melhor os testes e os cenários de validação do controlador.
