Para executar o programa é necessário executar o comando: "python main.py -e <caminho do arquivo de operacoes>"

O formato do arquivo de operações é o mesmo formato do qual foi dado na especificação do trabalho. Sendo necessário apenas este arquivo
de operações preenchido corretamente para executar o programa. Este arquivo serve para colocar os valores e instruções na "memoria.data"
que tem como papel ser a simulação da RAM.

Na raiz do projeto estão os arquivos de operação 'selecao.txt' e 'paridade.txt', o arquivo selecao.txt executa o selection sort 
de uma lista com n elementos. Enquanto o paridade.txt executa um algoritmo que dado um número verifica se é par ou impar, 
a paridade é retornada no endereco 0x02 tendo como 0 o número é par e caso for 1 o número é impar.

As instruções implementadas nesse trabalho foram: LOAD, ADD, SUB, MULT, DIV, STORE, JUMP, JUMP+, JUMP-, JUMPZ.

Para executar a ordenação por seleção foi criado o registrador EI, este registrador atua como endereçamento indireto.
Sua funcionalidade é guardar endereços. Quando utilizado a instrução (LOAD EI, <endereco>), esta transfere o endereco em si para o registrador EI.
Fazendo a instrução (LOAD EI), o AC recebe o conteudo que estiver no endereco de EI, por exemplo: o endereco 0x001 possui o valor 2, desta forma,
o registrador EI tem como conteudo o endereco 0x001 que quando aplicado a instrução LOAD EI, carrega o conteudo 2 
armazenado em 0x001 para o AC.

Assim como na instrução STORE, ao utilizar STORE EI, o conteudo de AC é escrito no endereco que o registrador EI contém.
Ou seja, se o AC tiver o valor 2 e EI tiver o endereco 0x002, o STORE irá escrever o valor 2 neste endereço.

O arquivo de operações da ordenação por seleção funciona da seguinte forma:
- O endereço 0x00 guarda o tamanho da lista
- Cada elemento da lista está guardado em um endereço de memória
- Os endereços 0x01 até o endereço N são todos reservados para os elementos da lista (no caso deste trabalho a lista pode ir até o endereço 0x00f por conta do endereço inicial das instruções e endereços auxiliares, porém, pode ser expandida ao mudar o endereço destes)
- O endereço 0x10 guarda o indice da base da lista, o 0x11 guarda o indice atual, o 0x12 guarda o indice do menor elemento e o 0x13 guarda o menor elemento
- As instruções começam no endereço 0x015