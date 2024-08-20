import sys

registradores = {
    'AC': 0,
    'MQ': 0,
    'C': 0,
    'Z': 0,
    'R': 0,
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

def escreve_instrucoes_memoria(arq, memoria, primeira_instrucao):
    offset = (TAM_LINHA * primeira_instrucao) + ENDERECO
    prox_inst = primeira_instrucao + 1
    num_instrucoes = 0
    for linha in arq:
        memoria.seek(offset)
        memoria.write(linha.rstrip().encode()) # linha[:-1] para ignorar a escrita do caracter '\n'
        offset = (TAM_LINHA * prox_inst) + ENDERECO
        prox_inst = prox_inst + 1

        memoria.seek(0)
        num_instrucoes+=1

    return num_instrucoes

def verifica_opcode(opcode, parametros, memoria):
    if opcode == 'LOAD':
        inst_load(parametros, memoria)
    elif opcode == 'ADD':
        inst_add(parametros, memoria)
    elif opcode == 'SUB':
        inst_sub(parametros, memoria)
    elif opcode == 'MOV':
        inst_mov(parametros)
    elif opcode == 'STORE':
        inst_store(parametros, memoria)
    elif opcode == 'CMP':
        inst_cmp(parametros)
    elif opcode == 'DIV':
        inst_div(parametros, memoria)
    elif opcode == 'MULT':
        inst_mult(parametros, memoria)

    print()
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

    print(f'Store a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

def inst_mov(parametros):
    if len(parametros) == 2:
        registrador_destino = parametros[0].upper()
        registrador_valor_origem = parametros[1].upper()

        registradores[registrador_destino] = registradores[registrador_valor_origem]

    print(f'Mov a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

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

    print(f'Add a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

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
    print(f'Sub a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

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

    print(f'Mult a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

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

    print(f'Div a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

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

    print(f'Load a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')

def executa_instrucoes(memoria, endereco_instrucao, num_instrucoes):
    offset = TAM_LINHA * endereco_instrucao + ENDERECO
    pc = endereco_instrucao + 1
    for i in range(num_instrucoes):
        memoria.seek(0)
        memoria.seek(offset)
        instrucao = memoria.readline().decode().rstrip().split()

        print(instrucao)
        
        instrucao = instrucao.split()
        opcode = instrucao[0]
        parametros = []
        for i in range(1, len(instrucao)):
            parametros.append(instrucao[i].rstrip(','))
        
        verifica_opcode(opcode, parametros, memoria)
        offset = TAM_LINHA * pc + ENDERECO
        pc+=1
        
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
                print(f'a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')
                le_operacoes(arq, memoria)
                print(f'a: {registradores['A']} b: {registradores['B']} ac: {registradores['AC']} mq: {registradores['MQ']}')
                memoria.close()
        else:
            raise Exception(f"Número incorreto de argumentos.\n{modo_uso}")
        arq.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)