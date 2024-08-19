def main():
    arq = open('memoria.data','w+b')
    for i in range(1024):
        mem = f'0x{hex(i)[2:].zfill(3)}'
        arq.write(mem)
        arq.write(' ')
        espaco = ' ' * 40
        arq.write(espaco)
        arq.write('\n')

    arq.seek(0)

if __name__ == '__main__':
    main()