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
    'EAUX': 0, # registrador extra
    'EBUX': 0, # registrador extra
    'EI': None
}

TAM_LINHA = 25 # tamanho total que cada linha da memoria.data possui 
ENDERECO = 6 # tamanho para que comece a palavra de memoria

VALOR_MAX = 2**40 - 1

def verifica_hex(valor):
    return '0x' in valor.lower()

def verifica_registrador(valor):
    return valor.upper() in registradores

def simula_carry_out(a, b, operacao):
    if operacao == 'add':
        resultado = a + b
        if resultado > VALOR_MAX:
            carry_borrow = 1
        else:
            carry_borrow = 2
    elif operacao == 'sub':
        resultado = a - b
        if resultado < 0:
            carry_borrow = 1  # In subtraction, this is often called a "borrow"
        else:
            carry_borrow = 2
    elif operacao == 'mult':
        resultado = a * b
        if resultado > VALOR_MAX:
            carry_borrow = 1
        else:
            carry_borrow = 2

    return carry_borrow, resultado

def verifica_zero(resultado):
    if resultado > 0:
        registradores['Z'] = 1
    elif resultado < 0:
        registradores['Z'] = -1
    else:
        registradores['Z'] = 0

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
    print(f"AC: {registradores['AC']} | MQ: {registradores['MQ']} | C: {registradores['C']} | R: {registradores['R']} | Z: {registradores['Z']} | EAUX: {registradores['EAUX']} | EBUX: {registradores['EBUX']} | EI: {registradores['EI']} ")
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
    memoria.write('END'.encode())

    return num_instrucoes

def operacao_dados(enderecos, memoria):
    decodificacao_instrucao(enderecos, memoria)
    if registradores['IR'] == 'LOAD':
        load(enderecos, memoria)
    elif len(enderecos) == 1:
        if registradores['IR'] == 'ADD':
            add()
        elif registradores['IR'] == 'SUB':
            sub()
        elif registradores['IR'] == 'STORE':
            store(enderecos[0], memoria)
        elif registradores['IR'] == 'DIV':
            div()
        elif registradores['IR'] == 'MULT':
            mult()
        elif registradores['IR'] == 'JUMP+':
            jump_plus(enderecos[0])
        elif registradores['IR'] == 'JUMP-':
            jump_minus(enderecos[0])
        elif registradores['IR'] == 'JUMP':
            jump(enderecos[0])
        elif registradores['IR'] == 'JUMPZ':
            jumpz(enderecos[0])
    else:
        raise Exception("Erro no formato das instrucoes.")
    memoria.seek(0)

def jump_plus(endereco):
    if registradores['AC'] > 0: # se o conteudo de AC for maior que 0, realiza desvio para o endereco
        registradores['PC'] = int(endereco[0], 16)
        registradores['MAR'] = registradores['PC']

def jump_minus(endereco):
    if registradores['AC'] < 0: # se o conteudo de AC for menor que 0, realiza desvio para o endereco
        registradores['PC'] = int(endereco[0], 16)
        registradores['MAR'] = registradores['PC']

def jump(endereco): # realiza desvio para o endereco dado
    registradores['PC'] = int(endereco[0], 16)
    registradores['MAR'] = registradores['PC']

def jumpz(endereco):
    if registradores['AC'] == 0: # se o conteudo de AC for igual a 0, realiza desvio para o endereco
        registradores['PC'] = int(endereco[0], 16)
        registradores['MAR'] = registradores['PC']

def store(endereco, memoria):
    memoria.seek(0)
    memoria.seek(registradores['MAR'] * TAM_LINHA + ENDERECO)
    if verifica_hex(endereco): # se STORE <endereco>
        memoria.write(str(registradores['AC']).encode())
    elif not verifica_hex(endereco): # se STORE <valor>
        memoria.write(str(endereco).encode())


def add():
    a = registradores['AC']
    b = int(registradores['MBR'])
    carry, resultado = simula_carry_out(a, b, 'add')
    registradores['AC'] = resultado
    registradores['C'] = carry
    verifica_zero(resultado)

def sub():
    a = registradores['AC']
    b = int(registradores['MBR'])
    borrow, resultado = simula_carry_out(a, b, 'sub')
    registradores['AC'] = resultado
    registradores['C'] = borrow
    verifica_zero(resultado)
   
def mult():
    a = registradores['MQ']
    b = int(registradores['MBR'])
    borrow, resultado = simula_carry_out(a, b, 'mult')
    registradores['MQ'] = resultado
    registradores['C'] = borrow
    verifica_zero(resultado)

def div():
    a = registradores['MQ']
    b = int(registradores['MBR'])
    quociente, resto, overflow = simula_divisao(a, b)
    if quociente is None:  # se houve divisao por zero
        registradores['C'] = 1
    else:
        registradores['MQ'] = quociente
        registradores['R'] = resto  # guarda o resto
        registradores['C'] = 1 if overflow else 2
        verifica_zero(quociente)

def simula_divisao(a, b):
    if b == 0: # trata divisao por zero
        raise Exception("Erro: Divisão por zero.")
    
    quociente = a // b
    resto = a % b
    
    # checa se passou do valor maximo
    if quociente > VALOR_MAX:
        quociente = quociente % (VALOR_MAX + 1)
        return quociente, resto, True
    
    return quociente, resto, False
 
def load(enderecos: list, memoria):
    if len(enderecos) == 1:
        if enderecos[0].upper() == 'EI':
            memoria.seek(0)
            memoria.seek(TAM_LINHA*int(registradores['EI'])+ENDERECO)
            registradores['AC'] = int(memoria.readline().decode().rstrip())

        elif verifica_registrador(enderecos[0]): # se LOAD <registrador>
            registradores['AC'] = registradores[enderecos[0].upper()]

        else: # se LOAD M(x) ou LOAD <valor>
            registradores['AC'] = int(registradores['MBR'])

    elif len(enderecos) == 2:
        if verifica_registrador(enderecos[0]): # se LOAD <registrador>, M(X) ou LOAD <registrador>, <valor>
            registradores[enderecos[0].upper()] = int(registradores['MBR'])
    else:
        raise Exception("ERRO: Instrução 'LOAD' inválida")

def decodificacao_instrucao(enderecos, memoria):
    if len(enderecos) == 2 and registradores['IR'] == 'LOAD':
        if verifica_registrador(enderecos[0]) and verifica_hex(enderecos[1]): # caso <registrador>, M(X)
            registradores['MAR'] = int(enderecos[1], 16)
            memoria.seek(TAM_LINHA*registradores['MAR']+ENDERECO)
            registradores['MBR'] = memoria.readline().decode().rstrip()

        elif verifica_registrador(enderecos[0]) and not verifica_hex(enderecos[1]): # caso <registrador>, <valor numerico>
            registradores['MBR'] = enderecos[1]
    elif len(enderecos) == 1:
        if verifica_registrador(enderecos[0]) and registradores['IR'] != 'LOAD':
            registradores['MBR'] = str(registradores[enderecos[0].upper()])

        elif verifica_hex(enderecos[0]):
            registradores['MAR'] = int(enderecos[0], 16)
            memoria.seek(TAM_LINHA*registradores['MAR']+ENDERECO)
            registradores['MBR'] = memoria.readline().decode().rstrip()
        
        elif not verifica_hex(enderecos[0]):
            registradores['MBR'] = enderecos[0]
        
    else:
        raise Exception("Instrução inválida")

def trata_enderecos(elementos_instrucao):
    enderecos = []
    for i in range(1, len(elementos_instrucao)):
        enderecos.append(elementos_instrucao[i].rstrip(','))
    return enderecos

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

    while registradores['IR'] != 'END':

        print('Registradores antes da instrução:\n')
        controle_fluxo_registradores()

        enderecos = trata_enderecos(registradores['MBR'].split())
        
        operacao_dados(enderecos, memoria)
        
        print(f"Registradores após a instrução ({instrucao}):\n")
        controle_fluxo_registradores()
        print('--------------------------------------------------\n')
   
        registradores['PC']+=1
        registradores['MAR'] = registradores['PC']
        instrucao = ciclo_busca(memoria)


def simula_ias(arq, memoria):
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
                simula_ias(arq, memoria)
                memoria.close()
        else:
            raise Exception(f"Número incorreto de argumentos.\n{modo_uso}")
        arq.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)