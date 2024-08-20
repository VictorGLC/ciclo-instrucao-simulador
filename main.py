import sys

registradores = {
    'AC': 0,
    'MQ': 0,
    'C': None,
    'Z': None,
    'R': None,
    'PC': 0,
    'IR': '',
    'MAR': '',
    'MBR': '',
    'A': 0,
    'B': 0,
}

TAM_LINHA = 40
ENDERECO = 6

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

def imprime_registradores():
    print(f"AC: {registradores['AC']} MQ: {registradores['MQ']} C: {registradores['C']} R: {registradores['R']} Z: {registradores['Z']} A: {registradores['A']} B: {registradores['B']} ")
    print(f"MAR: {registradores['MAR']} MBR: {registradores['MBR']} IR: {registradores['IR']} PC: {hex(registradores['PC'])}")
    
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

def escreve_instrucoes_memoria(arq, memoria, primeira_instrucao_endereco):
    offset = (TAM_LINHA * primeira_instrucao_endereco) + ENDERECO
    prox_inst = primeira_instrucao_endereco + 1
    num_instrucoes = 0
    for linha in arq:
        memoria.seek(offset)
        memoria.write(linha.rstrip().encode()) # linha[:-1] para ignorar a escrita do caracter '\n'
        offset = (TAM_LINHA * prox_inst) + ENDERECO
        prox_inst = prox_inst + 1

        memoria.seek(0)
        num_instrucoes+=1

    return num_instrucoes

def verifica_opcode(parametros, memoria):
    if registradores['IR'] == 'LOAD':
        inst_load(parametros, memoria)
    elif registradores['IR'] == 'ADD':
        inst_add(parametros, memoria)
    elif registradores['IR'] == 'SUB':
        inst_sub(parametros, memoria)
    elif registradores['IR'] == 'MOV':
        inst_mov(parametros)
    elif registradores['IR'] == 'STORE':
        inst_store(parametros, memoria)
    elif registradores['IR'] == 'CMP':
        inst_cmp(parametros)
    elif registradores['IR'] == 'DIV':
        inst_div(parametros, memoria)
    elif registradores['IR'] == 'MULT':
        inst_mult(parametros, memoria)

    memoria.seek(0)
    
def inst_store(parametros, memoria):
    if len(parametros) == 1:
        endereco_armazenamento = int(parametros[0], 16)
        memoria.seek(endereco_armazenamento * TAM_LINHA + ENDERECO)
        memoria.write(str(registradores['AC']).encode())
    else:
        endereco_armazenamento = int(parametros[1], 16)
        memoria.seek(endereco_armazenamento * TAM_LINHA + ENDERECO)
        registrador = parametros[0].upper()

        memoria.write(str(registradores[registrador]).encode())

def inst_mov(parametros):
    if len(parametros) == 2:
        registrador_destino = parametros[0].upper()
        registrador_valor_origem = parametros[1].upper()

        registradores[registrador_destino] = registradores[registrador_valor_origem]

def inst_add(parametros, memoria):
    if len(parametros) == 1:
        endereco_operando = int(parametros[0], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        registradores['AC'] += int(memoria.readline().rstrip())
    else:
        if not parametros[1].startswith('0x'): # se não estiver em hex, se trata de um numero inteiro e não a posição da memoria (Ex: ADD B, 10)
            valor = int(parametros[1])
        else:
            endereco_operando = int(parametros[1], 16)
            memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)
            valor = int(memoria.readline().rstrip())

        registrador = parametros[0].upper()

        registradores[registrador] += valor


def inst_sub(parametros, memoria):
    if len(parametros) == 1:
        endereco_operando = int(parametros[0], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        registradores['AC'] -= int(memoria.readline().rstrip())
    else:
        endereco_operando = int(parametros[1], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)
        valor = int(memoria.readline().rstrip())
        registrador = parametros[0].upper()

        if not parametros[1].startswith('0x'): # se não estiver em hex, se trata de um numero inteiro e não a posição da memoria (Ex: ADD B, 10)
            valor = int(parametros[1])

        registradores[registrador] -= valor

def inst_mult(parametros, memoria):
    if len(parametros) == 1:
        endereco_operando = int(parametros[0], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        registradores['MQ'] = int(memoria.readline().rstrip())
    else:
        endereco_operando = int(parametros[1], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        valor = int(memoria.readline().rstrip())
        registrador = parametros[0].upper()

        registradores[registrador] *= valor

def inst_div(parametros, memoria):
    if len(parametros) == 1:
        endereco_operando = int(parametros[0], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        registradores['MQ'] = int(memoria.readline().rstrip())
    else:
        endereco_operando = int(parametros[1], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        valor = int(memoria.readline().rstrip())
        registrador = parametros[0].upper()

        registradores[registrador] = int(registradores[registrador] / valor)

def inst_load(parametros: list, memoria):
    if len(parametros) == 1:
        endereco_operando = int(parametros[0], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        registradores['AC'] = int(memoria.readline().rstrip())
    else:
        endereco_operando = int(parametros[1], 16)
        memoria.seek(endereco_operando * TAM_LINHA + ENDERECO)

        valor = int(memoria.readline().rstrip())
        registrador = parametros[0].upper()

        registradores[registrador] = valor

def executa_instrucoes(memoria, primeira_instrucao_endereco, num_instrucoes):
    
    registradores['PC'] = primeira_instrucao_endereco
    for i in range(num_instrucoes):
        offset_endereco = TAM_LINHA * registradores['PC'] + ENDERECO
        memoria.seek(0)
        memoria.seek(offset_endereco)
        instrucao = memoria.readline().decode().rstrip()
        
        elementos_instrucao = instrucao.split()
        registradores['IR'] = elementos_instrucao[0]
        parametros = []
        for i in range(1, len(elementos_instrucao)):
            parametros.append(elementos_instrucao[i].rstrip(','))
        
        verifica_opcode(parametros, memoria)
        
        print(instrucao)
        while True:
            imprime_registradores()
            if inp := input('Pressione <ENTER> para continuar...\n') == '':
                break
        
        registradores['PC']+=1
def inst_cmp(parametros):
    if len(parametros) == 2:
        pass

def le_operacoes(arq, memoria):
    escreve_valores_memoria(arq, memoria)

    primeira_instrucao = int(arq.readline(), 16)
    memoria.seek(0)

    num_instrucoes = escreve_instrucoes_memoria(arq, memoria, primeira_instrucao)
    
    executa_instrucoes(memoria, primeira_instrucao, num_instrucoes)

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