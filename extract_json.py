import json


def organize_data(file):
           
        try :    
            f = open(file)
            data = json.load(f)
        
        except FileNotFoundError:
            return "Erreur : Le fichier spécifié est introuvable."
        
        except json.JSONDecodeError:
            return "Erreur : Le fichier JSON est mal formé."

        try : 
            topology = data['Topology'][0]       
            server = data["Server"]
            attackers = data["Attacker"]
            clients = data["Client"]
            listeners = data["Listeners"]
        
        except KeyError as e:
            return f"Erreur : Clé manquante dans le fichier JSON : {e}"

        try : 

            hosts = []
            switches = []
            links = []
        
            for subject, related_entities in topology.items():

                if subject.startswith('H'):  # Check if it's a host
                    hosts.append(subject)

                if subject.startswith('S'):  # Check if it's a switch
                    switches.append(subject)

                for related_entity in related_entities:
                    connection1 = (subject, related_entity)
                    connection2 = (related_entity, subject)
                    if connection1 and connection2 not in links:  # Avoid self-loops
                        links.append(connection1)
        
        except Exception as e:
            return f"Erreur lors du traitement des données : {e}"

            
        return {'Hosts': hosts, 'Switches': switches, 'Links': links, 'Server': server, 'Clients': clients,
                    'Attackers': attackers, 'Listeners': listeners}



print(organize_data("data1.json"))
data= organize_data("data1.json")

Hosts = data["Hosts"]
Switches = data["Switches"]
Links = data["Links"]
Server = data["Server"]
Clients = data["Clients"]
Attackers = data["Attackers"]
Listeners = data["Listeners"]

def attack_all(attackers):


    print("----------------- attacks ------------------------")

    for attacker in attackers :
        print(attacker[0][0],attacker[0][1], attacker[1],attacker[2], attacker[3])

    print("----------------- end of attacks ------------------------")


attack_all(Attackers)