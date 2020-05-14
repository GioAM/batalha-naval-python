import socket, pickle

# deve ser rodado pelo cliente

HOST = ''
PORT = 5555
tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

origem = (HOST, PORT)
tcp.bind(origem)
tcp.listen(2)
con, cliente = tcp.accept()

while True:
    mensagem = con.recv(1024)
    mensagem = mensagem.decode("UTF-8")
    if mensagem == "fim":
        break
    if mensagem.__contains__("write"):
        mensagem = mensagem[6:]
        texto = input(mensagem)
        con.send(str.encode(texto))
    else:
        print(mensagem, end="")