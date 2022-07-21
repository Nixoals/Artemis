import time
import os
import pytz
from datetime import datetime
import json
from gtts import gTTS
from playsound import playsound
#from face_recognition.face import who_is_in (maybe for future commit)

intents= json.loads(open(os.path.abspath(r'response_artemis/intents.json'), 'rb').read())

def actual_time_function(res):
  
  tz_Paris= pytz.timezone("Europe/Paris")
  now = datetime.now(tz_Paris)
  hours= [number for number in now.strftime("%H")]
  
  minutes=[number for number in now.strftime("%M")]
  hours_text= " heure"
  if hours[0] == "0" and hours[1] == "0":
    hours='minuit'
    hours_text= " "
  elif hours[0] == "1" and hours[1] == "2":
    hours='midi'
    hours_text= " "
    print(hours)
  elif hours[0]=="0" and hours[1] != "0":
    hours.remove("0")
    hours_text= "heure"
  hours= ''.join(hours)

  if minutes[0]=="0":
    minutes.remove("0")
  minutes= ''.join(minutes)
  current_time_converted = f'{res} : {hours} {hours_text} {minutes}' 
  response= gTTS(str(current_time_converted), lang='fr')

  return response


def detect_person():
  probability = who_is_in()

  totalPerson=[]
  if  "Nix" in probability :
    totalPerson.append('Vous, mon maître')
  
  
  if totalPerson==[]:
    response="Je n'ai détécté personne désolé"
  else:

    response= str('je détect' + ' mais aussi '.join(totalPerson))
  res = gTTS(response, lang='fr')
  return res


def allocate_request(tag, res):
  if tag == 'actual_time':
    response = actual_time_function(res)
    response.save('temp.mp3')
  #elif tag=='whoisin':
    #response=detect_person()
    #response.save('temp.mp3')
  else:
    response=gTTS(res, lang='fr')
    response.save(os.path.abspath(r'temp.mp3'))

  audio_file= os.path.abspath(r'temp.mp3')
  
  playsound(audio_file)
  os.remove(audio_file)


