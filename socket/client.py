#Cliente TCP
import socket
import rsa
from threading import Thread

global tcp_con

# Endereço das chaves publicas e provadas
client_public_key = "CLIENT_PUBLIC_KEY"
client_private_key = "CLIENT_PRIVATE_KEY"

arq = open(client_public_key,'rb')
txt = arq.read()
arq.close()

#Abre o arquivo da chave publica
with open(client_public_key, 'rb') as f:
    chave_publica_data = f.read()
    public_key = rsa.PublicKey.load_pkcs1(chave_publica_data, format='PEM')

#Função para receber as mensagens enviadas pelo servidor
def receber():
    global tcp_con
    while True:
        msg = tcp_con.recv(512)
        msgd = rsa.decrypt(msg, client_private_key) #Encripta a msg com a chave privada do client
        print ("Server:",msgd.decode())

# Função de envio
def enviar():
    global tcp_con
    print ('Para sair use CTRL+X\n')
    msg = input()
    while msg != '\x18':
        mensagem_codificada = msg.encode('utf-8') 
        msgEncriptada = rsa.encrypt(mensagem_codificada,public_key) # decodifica a msg com a chave publica do Server
        tcp_con.send(msgEncriptada)
        msg = input()
    tcp_con.close()
    
# Endereco IP do Servidor (maquina do servidor) 
SERVER = '192.168.137.115'

# Porta que o Servidor esta escutando
PORT = 5002

tcp_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (SERVER, PORT)
tcp_con.connect(dest)


t_rec = Thread(target=receber, args=())
t_rec.start()

t_env = Thread(target=enviar, args=())
t_env.start()