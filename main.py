import sys

ac = None
m = None
ibr = None
mar = None
mbr = None
ir = None
r = None
c = None
z = None
pc = None

TAM_LINHA = 40
ENDERECO = 6

INSTRUCOES = ['LOAD', 'LOAD M', 'LOAD MQ', 'LOAD MQ, M','ADD', 'SUB', 'MULT', 'MOV', 'DIV', 'CMP', 'STOR M']

def escreve_valores_memoria(arq, memoria):
    linha = arq.readline()
    while linha != '\n':
        linha = linha.split()
        valor = linha[0]
        endereco = linha[1]

        indice = int(endereco, 16)
        offset_linha = (TAM_LINHA * indice) + ENDERECO
        memoria.seek(offset_linha)
        memoria.write(valor.encode())
        memoria.seek(0)
        linha = arq.readline()

def criar_memoria():
    memoria = open('memoria.data','w+b')
    for i in range(1024):
        endereco = f'0x{hex(i)[2:].zfill(3)}' # zfill complementa com zeros a apos '0x' para ate ficar com 3 casas
        memoria.write(endereco.encode())
        memoria.write(' '.encode())
        espaco = ((' ' * 33) + '\n').encode()
        memoria.write(espaco)

    memoria.seek(0)

    return memoria


def escreve_instrucoes_memoria(arq, memoria, primeira_instrucao):
    offset = (TAM_LINHA * primeira_instrucao) + ENDERECO
    prox_inst = primeira_instrucao + 1
    memoria.seek(0)
    for linha in arq:
        memoria.seek(offset)
        memoria.write(linha[:-1].encode()) # linha[:-1] para ignorar a escrita do caracter '\n'
        memoria.seek(0)
        offset = (TAM_LINHA * prox_inst) + ENDERECO
        prox_inst = prox_inst + 1
    memoria.seek(0)    

def executa_instrucoes(memoria, endereco_instrucao):
    offset = TAM_LINHA * endereco_instrucao + ENDERECO
    memoria.seek(offset)
    print(memoria.readline())

def le_operacoes(arq, memoria):
    escreve_valores_memoria(arq, memoria)
    primeira_instrucao = int(arq.readline(), 16)
    escreve_instrucoes_memoria(arq, memoria, primeira_instrucao)
    executa_instrucoes(memoria, primeira_instrucao)

def main(nargs: int, args: list[str]) -> None:
    try:
        arq = open(args[2], 'r')
    except FileNotFoundError:
        print(f"Erro: não foi possivel encontrar o arquivo: {args[2]}")
    else:
        modo_uso = f"Modo de uso:\n$ {args[0]} -e nome_arq\n"

        if nargs == 3:
            flag = args[1]

            if flag != '-e':
                raise Exception(f"Flag {flag} inválida.\n{modo_uso}")
            else:
                memoria = criar_memoria()
                le_operacoes(arq, memoria)
                memoria.close()
        else:
            raise Exception(f"Número incorreto de argumentos.\n{modo_uso}")
        arq.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)