import time

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.link import  Link,OVSLink
from mininet.node import Controller, OVSSwitch, CPULimitedHost, OVSBridge
from mininet.link import TCLink
from mininet.cli import CLI
import subprocess
from extract_json import organize_data
import os.path



class MyTopo( Topo ):
    "Simple topology example."

    def build( self):
        "Create custom topo."
        # Add hosts and switches
        for i in range(len(Hosts)):
            self.addHost(Hosts[i])
        for i in range(len(Switches)):
            self.addSwitch(Switches[i])
        # Add links
        for i in range (len(Links)) :
            print(Links[i])
            left , right = Links[i][0],Links[i][1]
            self.addLink( left, right )




def start_mininet():
    #quand on travaille avec des OVSSwitch il faut spécifier les @IP, mais ce n'est pas le cas avec les OVSBridge
    process = subprocess.Popen("mn -c", shell=True, stdout=subprocess.PIPE)
    process.wait()
    #net = Mininet(topo= SingleSwitchTopo(2), controller=None, switch=OVSSwitch, waitConnected= False, link=TCLink )
    global net
    net = Mininet(topo=MyTopo(), switch=OVSBridge, waitConnected=False, controller=None)
    net.addNAT().configDefault()
    net.start()

def ping(x, y):
        """ ex: host_x = H1, host_y = 1 pour H2 """
        host_x, host_y = net.hosts[x], net.hosts[y] # dans le cas ou on veut passer le nombre du host en entrée pas le nom
        print("hoost",host_x)
        print(type(host_x))
        print(f" ------------- PING from {host_x}({host_x.IP()}) to {host_y}({host_y.IP()}) : -------------")
        for i in range(5): print(host_x.popen('ping -c1 %s' % host_y.IP()))

def launch_client(client_name, server_name, file):
    
    
    server , client = net.hosts[int(server_name[1:])], net.hosts[int(client_name[1:])]
    #h2 = net.get('h2')
    for i in range(5) : print(client.popen(f"python3 {file} -i {server.IP()} -m 'hello world' "))
    print(client, "---- request --->",server)

def launch_servers (servers):
    """Launch the server with the file mentioned in the JSON description"""
    
    for item in data["Server"] :
        for server, file  in item.items() :
            server_id = net.hosts[int(server[1:])]

            print(f"Le server c'est {server_id} de type {file[0]}")
            print(server_id.popen(f"python3 {file[0]} "))


def launch_all_clients(clients):

    for client in clients :
        launch_client(client[0][0],client[0][1], client[1] )
    print("----------------- end of requests ------------------------")

def attack (attacker_name, server_name, attack_type='tcp',port=53, time=3600):

    """Launch the attack by executing the MHDDOS script with the command : 
       python3 MHDDoS/start.py "attacker" "server":"port" 1 "time" in the attacker's terminal"""
    
    server, attacker = net.hosts[int(server_name[1:])], net.hosts[int(attacker_name[1:])]
    
    server_ip = server.IP() #ip of the server


    command = f"python3 MHDDoS/start.py {attack_type} {server_ip}:{port} 1 {time} " 
    print(command)
    print(attacker.popen(command))
    print(attacker, "------ attack ----->", server)


def attack_all(attackers):


    print("----------------- attacks ------------------------")

    for attacker in attackers :
        print(attacker[0][0],attacker[0][1], attacker[1],attacker[2], attacker[3])

    print("----------------- end of attacks ------------------------")


def tshark(host, output='output.pcap'):
    """ lancer le tshark pour chaque listener  """

    
    
    host = net.hosts[int(host[1:])] # on recupére l'objet host 
    
    filename = f"{host}_{output}"
    
    with open(filename, 'wb') as file:  # giving the wb right for the file 
        pass

    command = f"tshark -w {filename} " 
    print(host)
    print(host.popen(command)) # cmd of the host : "tshark -w hostname_output.pcap"
    print("end")
    #time.sleep(20)



def tshark_all(listners,output='output.pcap'):
    
    """lunching the tshark for all the listner"""

    for host in listners :
        tshark(host,output)




if __name__ == '__main__':

    data = organize_data("data1.json")
    global Hosts, Switches, Links, Server, Clients, Attackers, Listners
    Hosts = data["Hosts"]
    Switches = data["Switches"]
    Links = data["Links"]
    Server = data["Server"]
    Clients = data["Clients"]
    Attackers = data["Attackers"]
    Listeners = data["Listeners"]


    start_mininet()

    #ping(1,0)
    launch_servers(data["Server"])
    #attack("H1","H0")
    #tshark("H1")

    tshark_all(Listeners)
    #time.sleep(10)
    launch_all_clients(Clients)
    #time.sleep(10)
    #attack_all(Attackers)
    cli = CLI(net)
