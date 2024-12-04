#Servidor TCP
import socket
from threading import Thread

global tcp_con
import rsa


# A chave publica da pessoa para quem vou enviar a mensagem
client_public_key_address = "/home/jhonatan/github/Fateclando/chaves/clientPub.txt"
with open(client_public_key_address, 'rb') as file:
    public_key_file = file.read()
client_public_key = rsa.PublicKey.load_pkcs1(public_key_file, format='PEM')

# Caminho para a minha chave privada
server_private_key_address = "/home/jhonatan/github/Fateclando/chaves/serverPri.txt"
with open(server_private_key_address, 'rb') as file:
    private_server_file = file.read()
server_private_key = rsa.PrivateKey.load_pkcs1(private_server_file, format='PEM')

        
def enviar():
    global tcp_con
    print('Para sair use CTRL+X\n')
    msg = input()
    while msg != '\x18':
        codified_message = msg.encode('utf-8')
        cripted_message = rsa.encrypt(codified_message, client_public_key)
        tcp_con.send(cripted_message)
        msg = input()
    tcp_con.close()

def receber():
    global tcp_con
    while True:
        msg = tcp_con.recv(1024)
        if not msg:
            break
        msgd = rsa.decrypt(msg, server_private_key)
        print("Cliente:", msgd.decode())

# Endereco IP do Servidor
HOST = '192.168.137.116'

# Porta que o Servidor vai escutar
PORT = 5002

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

print('Servidor online')
tcp_con, cliente = tcp.accept()
print('Conectado por', cliente)

t_rec = Thread(target=receber)
t_rec.start()

t_env = Thread(target=enviar)
t_env.start()

t_rec.join()
t_env.join()

print('Finalizando conexao com', cliente)
tcp_con.close()