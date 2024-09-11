Para executar o programa é necessário executar o comando: "python main.py -e <caminho do arquivo de operacoes>"

O formato do arquivo de operações é o mesmo formato do qual foi dado na especificação do trabalho. Sendo necessário apenas este arquivo
de operações preenchido corretamente para executar o programa. Este arquivo serve para colocar os valores e instruções na "memoria.data"
que tem como papel ser a simulação da RAM.

Na raiz do projeto estão os arquivos de operação selecao.txt e o paridade.txt, o arquivo selecao.txt executa o selection sort 
de uma lista com 4 elementos. Enquanto o paridade.txt é um algoritmo que verifica a paridade de um número, a paridade é vista 
na célula 0x02 que se for 0, o número é par, caso contrario, se for 1 o número é impar.

As instruções implementadas nesse trabalho foram: LOAD, ADD, SUB, MULT, DIV, STORE, JUMP+, JUMP-, JUMP e JUMPZ.

Para realizar a ordenação por seleção foi criado o registrador EI, este registrador atua como um endereçamento indireto.
Sua funcionalidade é guardar endereços. Quando utilizado com LOAD EI, <endereco> transfere o endereco em si para o EI.
Fazendo LOAD EI, o AC recebe o conteudo que estiver no endereco de EI, por exemplo: o endereco 0x001 tem o valor 2, portanto,
o registrador EI recebe 0x001 que quando aplicado a instrução LOAD EI, carrega o conteudo 2 para o AC.

Assim como na instrução STORE, ao utilizar STORE EI, o conteudo de AC é escrito no endereco que o registrador EI contém.
Ou seja, se o AC tiver o valor 2 e EI tiver o endereco 0x002, o STORE irá escrever o valor 2 neste endereço.

O arquivo de operações da ordenação por seleção funciona da seguinte forma:
- O endereço 0x00 guarda o tamanho da lista
- Cada elemento da lista está guardado em um endereço de memória
- Os endereços 0x01 até o endereço n-1 são todos reservados para os elementos da lista
- O endereço 0x10 guarda o indice da base da lista, o 0x11 guarda o indice atual, o 0x12 guarda o indice do menor elemento e o 0x13 guarda o menor elemento
