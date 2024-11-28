#python3 version
import rsa
import os

print ('Gerador de chaves assimetricas')
size = 256
end = os.path.join(os.getcwd(), 'chaves')  # Isso irá criar o caminho para o diretório chaves

# Verificar se a pasta 'chaves' existe, caso contrário, cria
if not os.path.exists(end):
    os.makedirs(end)

nome = input('Nome do arquivo: ')

##gero as chaves com o tamanho informado
(pub,pri) = rsa.newkeys(int(size))

##crio o arquivo pub
arqnomepub = os.path.join(end, nome + 'Pub.txt')
#codifico o exponente e modulo da chave para o formate PEM
arq = open(arqnomepub,'wb')
arq.write(pub.save_pkcs1(format='PEM'))
arq.close()

##crio o arquivo pri
arqnomepri = os.path.join(end, nome + 'Pri.txt')
arq = open(arqnomepri,'wb')
##codifico o exponente e modulo da chave para o formate PEM
arq.write(pri.save_pkcs1(format='PEM'))
arq.close()

print ('Chaves geradas com sucesso')
print (arqnomepub)
print (arqnomepri)






