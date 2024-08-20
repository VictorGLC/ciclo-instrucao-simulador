def main():
    arq = open('memoria.data','w+b')
    for i in range(1024):
        mem = f'0x{hex(i)[2:].zfill(3)}'.encode()
        arq.write(mem)
        arq.write(' '.encode())
        espaco = ((' ' * 40) + '\n').encode()
        arq.write(espaco)

    arq.seek(0)

if __name__ == '__main__':
    main()