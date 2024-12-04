#Cliente TCP
import socket
import rsa
from threading import Thread

global tcp_con

# Endereço das chaves publicas e privadas
serverPubKey = "/home/jhonatan/github/Fateclando/chaves/serverPub.txt"
clientPriKey = "/home/jhonatan/github/Fateclando/chaves/clientPri.txt"

# Abre o arquivo da chave pública do servidor
with open(serverPubKey, 'rb') as f:
    chave_publica_data = f.read()
public_key = rsa.PublicKey.load_pkcs1(chave_publica_data, format='PEM')

# Abre o arquivo da chave privada do cliente
with open(clientPriKey, 'rb') as t:
    chave_privada_data = t.read()
private_key = rsa.PrivateKey.load_pkcs1(chave_privada_data, format='PEM')

# Função para receber as mensagens enviadas pelo servidor
def receber():
    global tcp_con
    while True:
        msg = tcp_con.recv(512)
        if not msg:
            break
        msgd = rsa.decrypt(msg, private_key)
        print("Server:", msgd.decode())

# Função de envio
def enviar():
    global tcp_con
    print('Para sair use CTRL+X\n')
    msg = input()
    while msg != '\x18':
        mensagem_codificada = msg.encode('utf-8')
        msgEncriptada = rsa.encrypt(mensagem_codificada, public_key)
        tcp_con.send(msgEncriptada)
        msg = input()
    tcp_con.close()

# Endereco IP do Servidor
SERVER = '127.0.0.1'

# Porta que o Servidor esta escutando
PORT = 5002

tcp_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (SERVER, PORT)
tcp_con.connect(dest)

t_rec = Thread(target=receber)
t_rec.start()

t_env = Thread(target=enviar)
t_env.start()

t_rec.join()
t_env.join()