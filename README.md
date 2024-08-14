# Simulador de ciclo de instrução - IAS
Projeto de implementaçao de simulador de ciclo de instruções baseado na arquitetura do computador IAS.

## Objetivo

Desenvolver um programa que simule o comportamento dos registradores de um processador em um ciclo de instrução ao executar uma sequência de comandos de linguagem de máquina. Os registradores devem armazenar dados temporariamente para que tais comandos sejam executados. Além disso, a quantidade de registradores deve ser suficiente para suportar a execução dos comandos solicitados.

## Descrição

O simulador desenvolvido deve executar operações básicas de linguagem de máquina, como adição, subtração, divisão, multiplicação, transferência de dados, e desvio de fluxo. Todas as instruções do algoritmo e os dados contidos nele devem estar armazenados em memória RAM.

Para fins de implementação, os comandos devem ser armazenados na RAM sequencialmente em um local distinto de onde os dados serão armazenados.

O programa (simulador) deve receber como entrada um algoritmo para a solução de um problema. Além disso, o programa deve pedir que o usuário forneça o endereço da primeira instrução do algoritmo. A primeira instrução é armazenada no endereço fornecido e as demais instruções são alocadas nos endereços subsequentes. O algoritmo pode ser fornecido por meio de um arquivo.

A cada execução de uma instrução, o conteúdo dos Registradores PC, MAR, MBR e IR deve ser exibido, assim como os demais registradores de uso geral utilizados para a resolução do problema.

O simulador deverá executar o algoritmo do método de ordenação por Seleção e outro à sua escolha.

Em seguida, os dados utilizados neste algoritmo são armazenados.

O programa (simulador) deve receber como entrada um arquivo texto com os dados e a sequência de comandos. A linha 0 até a linha n-1 do arquivo informam os dados e a posição na memória em que estão armazenados. A linha n do arquivo indica o endereço na memória do primeiro comando a ser executado. As linhas subsequentes indicam os demais comandos da sequência, sendo que a posição na memória está implícita de acordo com a posição do primeiro comando.

Após a leitura deste arquivo, o programa em linguagem de máquina e os dados utilizados nele estão representados em uma memória (ou vetor no programa). Este vetor deve simular o armazenamento de dados na RAM. Cada posição do vetor é endereçada por um valor no sistema hexadecimal. O mapeamento entre as posições do vetor da memória ocorre da seguinte maneira: a primeira posição do vetor equivale ao endereço `0x00`, a segunda equivale ao endereço `0x01` e assim sucessivamente. Por exemplo, a décima primeira posição do vetor equivale ao endereço `0x0A` da RAM. Um exemplo de arquivo texto de entrada é mostrado a seguir:

```
3 0x02
4 0x05
10 0x06

0x0A
LOAD A, 0x05
ADD A, 0x02
MOV B, A
MULT B, 0x06
ADD B, 5
STORE B, 0x1B
```

## Considerações

- Todos os dados envolvidos nos comandos devem ser inteiros.
- O conjunto de instruções do computador IAS, assim como o tamanho das palavras e instruções.
- Endereçamento Imediato e Direto.
- Os seguintes registradores:
  - **AC**: Acumulador
  - **M**: Multiplicador
  - **R**: Resto da divisão
  - **C**: Carry out (1: houve carry; 2: não houve carry)
  - **Z**: Resultado zero (-1: resultado negativo; 0: resultado igual a zero; 1: resultado positivo)
  - **PC**: Program Counter
  - **IR**: Instruction Register
  - **MAR**: Memory Address Register
  - **MBR**: Memory Buffer Register
- Não há chamada de procedimento.
- Não é necessário salvar o contexto do processador para restaurá-lo posteriormente.
- Não há interrupções.

## Observações Finais

Como o objetivo deste projeto é simular o comportamento dos registradores de um processador, o conteúdo de todos os registradores deve ser impresso em tela para cada comando da sequência. Para melhor visualizar a saída do programa, controle o fluxo de execução do algoritmo teclando `<ENTER>` entre a execução de dois comandos.

Antes de executar o primeiro comando, o conteúdo dos registradores deve ser exibido em tela. Lembre-se que neste instante somente o registrador PC possuirá conteúdo válido.