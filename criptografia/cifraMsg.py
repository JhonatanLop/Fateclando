#python3 version
import rsa
import os
import glob

print('\\-------------------------------//')
print('**Prj Banco de Dados Distribuidos**')
print('\\-------------------------------//')
print('Cifrador de mensagens')

# Caminho da pasta de chaves
chaves_dir = os.path.join(os.getcwd(), 'chaves')

chave_publica = None
for arquivo in glob.glob(os.path.join(chaves_dir, '*Pub*.txt')):
    chave_publica = arquivo
    break

if not chave_publica:
    print('Erro: Nenhuma chave pública encontrada na pasta "chaves".')
    exit()

print(f'Chave pública encontrada: {chave_publica}')

# Lê a mensagem a ser cifrada
msg = input('Mensagem a ser cifrada: ').encode('utf-8')

# Caminho da pasta 'msg'
msg_dir = os.path.join(os.getcwd(), 'msg')

# Solicita o nome para o arquivo da mensagem
nome_arquivo_msg = input('Nome do arquivo da mensagem cifrada (ex.: msg1.txt): ')
arqnomemsg = os.path.join(msg_dir, nome_arquivo_msg)

# Lê o conteúdo da chave pública
with open(chave_publica, 'rb') as arq:
    txt = arq.read()

# Decodifica para o formato de chave pública
pub = rsa.PublicKey.load_pkcs1(txt, format='PEM')

# Cifra a mensagem
msgc = rsa.encrypt(msg, pub)

# Cria a pasta 'msg' se ela não existir
os.makedirs(msg_dir, exist_ok=True)

# Salva a mensagem cifrada no arquivo
with open(arqnomemsg, 'wb') as arq:
    arq.write(msgc)

print(f'Mensagem cifrada no arquivo: {arqnomemsg}')



