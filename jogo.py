from models import *

jogador1 = Jogador(True)
jogador2 = Jogador(False)


jogador1.qual_o_nome()
jogador2.qual_o_nome()

while not jogador1.ganhou or not jogador2.ganhou:
    jogador1.jogada()
    if jogador1.ganhou:
        break
    jogador2.jogada()

jogador1.final()
jogador2.final()