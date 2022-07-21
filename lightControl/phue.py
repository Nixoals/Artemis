from phue import Bridge
from phue import Group
import json

b = Bridge('192.168.1.10') #Add the Ip Adress of the philips Hue bridge

b.connect()

response = b.get_api()

"""
command.json contain the scene, name & group and the command to run.
If you want to get the response from your hueBrigde and all the associated data,
uncomment the next few lines
"""
#with open('parsedResponse.json', 'w') as f:
#    json.dump(response, f, indent=4)
#
#print(json.dumps(response, indent=4))


with open("command/command.json", "r") as f:
    command= json.load(f)
    
#add as many command as you want as long as they are in the command.json
def lightsController(response):
    if response in command["lightControl"]:
        if command["lightControl"][response]["set_light"] == "True" :
            for group in command["lightControl"][response]["group_name"]:
                lightgroup = Group(b, group)
                scene=command["lightControl"][response]["scene_name"]
                b.run_scene(group_name=group, scene_name = scene, transition_time=6)
        else:
            for group in command["lightControl"][response]["group_name"]:
                lightgroup = Group(b, group)
                lightgroup.on= False
        



