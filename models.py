import socket, os
from random import choice, random

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Jogador:
    def __init__(self, is_host, host=""):
        self.mapa = Mapa()
        self.ganhou = False
        self.is_host = is_host
        port = 5555

        if is_host:
            print("Mapa do Jogador")
            print(" ")
            self.mapa.mostrar(self)
        else:
            destino = (host, port)
            tcp.connect(destino)
            tcp.send(str.encode("Mapa do Jogador\n"))
            self.mapa.mostrar(self)

    def qual_o_nome(self):
        if self.is_host:
            print("Qual o nome?")
            self.nome = input()
        else:
            tcp.send(str.encode("write-Qual o seu nome?"))
            mensagem = tcp.recv(1024)
            mensagem = mensagem.decode("UTF-8")
            self.nome = mensagem

    def jogada(self):
        if self.is_host:
            print('Vez do Jogador', self.nome)
            x = 0
            y = 0
            self.mapa.mostrar(self)
            x = int(input('Linha:'))
            y = int(input('Coluna:'))
            if x <= 0 or x > 10 or y <= 0 or y > 10:
                print("Números não aceitos, perdeu a vez")
            else:
                x = x - 1
                y = y - 1
                self.mapa.mapa[x][y].atirar()
                if self.mapa.mapa[x][y].valor == 'X':
                    print("Acertou uma parte do navio!")
                    print("")
                else:
                    print("Errou a parte do navio!")
                    print("")

                print("Mapa do Jogador %s" % (self.nome))
                self.mapa.mostrar(self)
                self.acertou()
        else:
            tcp.send(str.encode('Vez do Jogador ' + self.nome + '\n'))
            x = 0
            y = 0
            self.mapa.mostrar(self)
            tcp.send(str.encode('write-Linha:'))
            mensagem = tcp.recv(1024).decode("UTF-8")
            x = int(mensagem)
            tcp.send(str.encode('write-Coluna:'))
            mensagem = tcp.recv(1024).decode("UTF-8")
            y = int(mensagem)
            if x <= 0 or x > 10 or y <= 0 or y > 10:
                tcp.send(str.encode("Números não aceitos, perdeu a vez"))
            else:
                x = x - 1
                y = y - 1
                self.mapa.mapa[x][y].atirar()
                if self.mapa.mapa[x][y].valor == 'X':
                    tcp.send(str.encode("Acertou uma parte do navio!\n\n"))
                else:
                    tcp.send(str.encode("Errou a parte do navio!\n\n"))

                tcp.send(str.encode("Mapa do Jogador " + (self.nome) + '\n'))
                self.mapa.mostrar(self)
                self.acertou()


    def acertou(self):
        for navio in self.mapa.navios:
            ganhou = True
            for posicoes in navio:
                if not self.mapa.mapa[int(posicoes[0])][int(posicoes[1])].atingido:
                    ganhou = False
            if ganhou:
                self.ganhou = True
                break

    def final(self):
        if self.is_host:
            if self.ganhou:
                print("Parabéns %s, você venceu"%(self.nome))
            else:
                print("%s, você perdeu"%(self.nome))
        else:
            if self.ganhou:
                tcp.send(str.encode("Parabéns" + self.nome + "você venceu\n"))
            else:
                tcp.send(str.encode(self.nome + ", você perdeu\n"))
            tcp.send(str.encode("fim"))
            tcp.close()
#
class Quadrado:
    def __init__(self):
        self.atingido = False
        self.valor = '-'

    def __str__(self):
        if self.atingido:
            return self.valor
        return '~'

    def mostrar(self):
        if self.atingido:
            return self.valor
        return '~'

    def atirar(self):
        self.atingido = True

class Mapa:

    def __init__(self, x=10, y=10, numero_de_navios=3):
        self.mapa = []
        self.x = x
        self.y = y
        self.numero_de_navios = numero_de_navios
        self.navios = []

        for i in range(self.x):
            self.mapa.append([]);
            for j in range(self.y):
                quadrado = Quadrado()
                self.mapa[i].append(quadrado)
        self.adicionar_navios()

    def mostrar(self, jogador):
        if jogador.is_host:
            print("")
            print("   1 2 3 4 5 6 7 8 9 10")
            for i in range(self.x):
                print(i+1, end="  ")
                for j in range(self.y):
                    print(self.mapa[i][j], end=" ")
                print('')

            print("")
        else:
            tcp.send(str.encode(("\n")))
            tcp.send(str.encode("   1 2 3 4 5 6 7 8 9 10 \n"));
            for ia in range(self.x):
                frase = str(ia + 1) + "   "
                tcp.send(str.encode(frase))
                for ja in range(self.y):
                    tcp.send(str.encode(self.mapa[ia][ja].mostrar() + " "));
                tcp.send(str.encode('\n'));

    def adicionar_navios(self):
        for i in range(self.numero_de_navios):
            navio_adicionado = False

            while not navio_adicionado:
                x1 = int(random() * self.x)
                y1 = int(random() * self.y)
                if self.mapa[x1][y1].valor == 'X':
                    navio_adicionado = False
                    continue
                posicao = choice(['v','h'])

                if posicao == 'v':
                    x2 = x1 + 1
                    x3 = x2 + 1
                    y3 = y2 = y1
                else:
                    y2 = y1 + 1
                    y3 = y2 + 1
                    x3 = x2 = x1
                if x2 >= 10 or y2 >= 10 or x3 >= 10 or y3 >= 10:
                    navio_adicionado = False
                    continue

                if self.mapa[x2][y2].valor == 'X' or self.mapa[x3][y3].valor == 'X':
                    navio_adicionado = False
                    continue
                navio = [[x1,y1],[x2,y2],[x3,y3]]
                self.navios.append(navio)
                self.mapa[x1][y1].valor = 'X'
                self.mapa[x2][y2].valor = 'X'
                self.mapa[x3][y3].valor = 'X'
                navio_adicionado=True