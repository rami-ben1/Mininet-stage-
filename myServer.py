import socket, optparse

print("on est dans le serveur")
parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='10.0.0.1')
parser.add_option('-p', dest='port', type='int', default=125)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((options.ip, options.port))

f = open('foo.txt','w')
f.write(f"Serveur en écoute sur {options.ip}:{options.port} \n")
while True:
    data, addr = s.recvfrom(512)
    print(f"Reçu de {addr}: {data.decode()}")  # Ajout de l'impression pour diagnostiquer
    f.write("%s: %s\n" % (addr, data.decode()))  # Décodage des données reçues en tant que chaîne
    f.flush()