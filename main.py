import sys

registradores = {
    'AC': 0,
    'MQ': 0,
    'C': None,
    'Z': None,
    'R': None,
    'PC': 0,
    'IR': '',
    'MAR': None,
    'MBR': '',
    'A': 0, # registrador extra
    'B': 0, # registrador extra
}

TAM_LINHA = 25 # tamanho total que cada linha da memoria.data possui 
ENDERECO = 6 # tamanho para que comece a palavra de memoria

def criar_memoria():
    memoria = open('memoria.data','w+b')
    for i in range(1024):
        endereco = f'0x{hex(i)[2:].zfill(3)}' # zfill complementa com zeros a apos '0x' para ate ficar com 3 casas
        memoria.write(endereco.encode())
        espaco = ((' ' * (TAM_LINHA-ENDERECO)) + '\n').encode()
        memoria.write(espaco)

    memoria.seek(0)

    return memoria

def imprime_registradores():
    print(f"AC: {registradores['AC']} | MQ: {registradores['MQ']} | C: {registradores['C']} | R: {registradores['R']} | Z: {registradores['Z']} | A: {registradores['A']} | B: {registradores['B']} ")
    print(f"MAR: {hex(registradores['MAR'])} | MBR: {registradores['MBR']} | IR: {registradores['IR']} | PC: {hex(registradores['PC'])}")
    
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

def escreve_instrucoes_memoria(arq, memoria):
    offset = (TAM_LINHA * registradores['PC']) + ENDERECO
    prox_inst = registradores['PC'] + 1
    num_instrucoes = 0
    for linha in arq:
        memoria.seek(offset)
        memoria.write(linha.rstrip().encode()) # linha[:-1] para ignorar a escrita do caracter '\n'
        offset = (TAM_LINHA * prox_inst) + ENDERECO
        prox_inst = prox_inst + 1

        memoria.seek(0)
        num_instrucoes+=1
    
    memoria.seek(offset)
    memoria.write('HALT'.encode())

    return num_instrucoes

def operacao_dados(parametros, memoria):
    if registradores['IR'] == 'LOAD':
        load(parametros)
    elif registradores['IR'] == 'ADD':
        add(parametros)
    elif registradores['IR'] == 'SUB':
        sub(parametros)
    elif registradores['IR'] == 'MOV':
        mov(parametros)
    elif registradores['IR'] == 'STORE':
        store(parametros, memoria)
    elif registradores['IR'] == 'DIV':
        div(parametros)
    elif registradores['IR'] == 'MULT':
        mult(parametros)
    elif registradores['IR'] == 'JUMP+':
        jump_plus(parametros)

    memoria.seek(0)

def jump_plus(parametros):
    if registradores['AC'] >= 0:
        registradores['PC'] = int(parametros[0], 16)
        registradores['MAR'] = registradores['PC']

def store(parametros, memoria):
    memoria.seek(0)
    if len(parametros) == 1:
        memoria.seek(registradores['MAR'] * TAM_LINHA + ENDERECO)
        memoria.write(registradores['MBR'].encode())
    elif len(parametros) == 2:
        memoria.seek(registradores['MAR'] * TAM_LINHA + ENDERECO)

        memoria.write(registradores['MBR'].encode())

def mov(parametros):
    if len(parametros) == 2:
        registrador_destino = parametros[0].upper()
        registrador_valor_origem = parametros[1].upper()

        registradores[registrador_destino] = registradores[registrador_valor_origem]

def add(parametros):
    if len(parametros) == 1:
        registradores['AC'] += int(registradores['MBR'])
    else:
        registrador = parametros[0].upper()

        registradores[registrador] += int(registradores['MBR'])

def sub(parametros):
    if len(parametros) == 1:
        registradores['AC'] -= int(registradores['MBR'])
    else:
        registrador = parametros[0].upper()

        registradores[registrador] -= int(registradores['MBR'])

def mult(parametros):
    if len(parametros) == 1:
        registradores['MQ'] *= int(registradores['MBR'])
    else:
        registrador = parametros[0].upper()

        registradores[registrador] *= int(registradores['MBR'])

def div(parametros):
    if len(parametros) == 1:
        registradores['MQ'] = int(registradores['MBR'])
    else:
        registrador = parametros[0].upper()

        registradores[registrador] = int(registradores[registrador] / int(registradores['MBR']))

def load(parametros: list):
    if len(parametros) == 1:
        registradores['AC'] = int(registradores['MBR'])
    else:
        registrador = parametros[0].upper()

        registradores[registrador] = int(registradores['MBR'])

def verifica_hex(valor):
    return valor.startswith('0x')

def verifica_registrador(valor):
    return valor.upper() in registradores

def decodificacao_instrucao(parametros, memoria):
    if len(parametros) == 2:
        if verifica_registrador(parametros[0]) and verifica_registrador(parametros[1]):
            registradores['MBR'] = str(registradores[parametros[1].upper()])

        elif verifica_registrador(parametros[0]) and verifica_hex(parametros[1]) and registradores['IR'] == 'STORE':
            registradores['MAR'] = int(parametros[1], 16)
            registradores['MBR'] = str(registradores[parametros[0].upper()])

        elif verifica_registrador(parametros[0]) and verifica_hex(parametros[1]):
            registradores['MAR'] = int(parametros[1], 16)
            memoria.seek(TAM_LINHA*registradores['MAR']+ENDERECO)
            registradores['MBR'] = memoria.readline().decode().rstrip()

        elif not verifica_hex(parametros[1]):
            registradores['MBR'] = parametros[1]

    elif len(parametros) == 1:
        if verifica_registrador(parametros[0]):
            registradores['MBR'] = str(registradores[parametros[0].upper()])

        elif verifica_hex(parametros[0]) and registradores['IR'] == 'STORE':
            registradores['MAR'] = int(parametros[0], 16)
            registradores['MBR'] = str(registradores['AC'])

        else:
            registradores['MAR'] = int(parametros[0], 16)
            memoria.seek(TAM_LINHA*registradores['MAR'] + ENDERECO)
            registradores['MBR'] = memoria.readline().decode().rstrip()

def trata_enderecos(elementos_instrucao):
    parametros = []
    for i in range(1, len(elementos_instrucao)):
        parametros.append(elementos_instrucao[i].rstrip(','))
    return parametros

def controle_fluxo_registradores():
    while True:
        imprime_registradores()
        if inp := input('Pressione <ENTER> para continuar...\n') == '':
            break

def ciclo_busca(memoria):
    offset_endereco = TAM_LINHA * registradores['MAR'] + ENDERECO
    memoria.seek(0)
    memoria.seek(offset_endereco)
    instrucao = memoria.readline().decode().rstrip()

    registradores['MBR'] = instrucao
    elementos_instrucao = registradores['MBR'].split()
    registradores['IR'] = elementos_instrucao[0]

    return instrucao

def executa_instrucoes(memoria):
    registradores['MAR'] = registradores['PC']

    instrucao = ciclo_busca(memoria)

    while registradores['IR'] != 'HALT':

        print('Registradores antes da instrução:\n')
        controle_fluxo_registradores()

        parametros = trata_enderecos(registradores['MBR'].split())
        
        decodificacao_instrucao(parametros, memoria)
        operacao_dados(parametros, memoria)
        
        print(f"Registradores após a instrução ({instrucao}):\n")
        controle_fluxo_registradores()
        print('--------------------------------------------------\n')
   
        registradores['PC']+=1
        registradores['MAR'] = registradores['PC']

        instrucao = ciclo_busca(memoria)


def le_operacoes(arq, memoria):
    escreve_valores_memoria(arq, memoria)

    registradores['PC'] = int(arq.readline(), 16)
    memoria.seek(0)

    escreve_instrucoes_memoria(arq, memoria)
    
    executa_instrucoes(memoria)

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