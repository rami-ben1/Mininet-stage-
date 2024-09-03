import socket, optparse

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='10.0.0.1')
parser.add_option('-p', dest='port', type='int', default=125)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = options.msg.encode()  # Conversion de la chaîne en bytes
print(f"Envoi de {options.msg} à {options.ip}:{options.port}")  # Ajout de l'impression pour diagnostiquer
s.sendto(message, (options.ip, options.port))
