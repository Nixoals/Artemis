#!/usr/bin/env python3

import argparse
import os
import queue
from time import time
import sounddevice as sd
import vosk
import sys
import json
import time
from lightControl.phue import lightsController
from response_artemis.artemisAI import responseAI
  

with open('command/command.json', 'r') as f:
  command = json.load(f)


q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

"""

Download the vosk model fr in the root directory
and rename the folder => 'VoskModel'

"""

model = vosk.Model('VoskModel')
rec = vosk.KaldiRecognizer(model, 48000)

def recognize():
    
    with sd.RawInputStream(samplerate=48000, blocksize = 8000, device='default', dtype='int16', channels=1, callback=callback):

            parsing=True
            while parsing:
                data = q.get()
               
                if rec.AcceptWaveform(data):
                    finalResult = rec.Result()
                    output= json.loads(finalResult)
                    
                    print(output['text'])

                    for value in command["lightControl"]:
                        if value in output['text']:
                            lightsController(value)
                            time.sleep(0.2)
                            q.queue.clear()
                            parsing=False
                    
                    if output['text'] not in command['lightControl']:
                        responseAI(output['text'])
                        q.queue.clear()
                        parsing=False
                        break
                    parsing=False if output['text']=="" else print('#'*25 +'\nSending parsed results! \n'+'#'*25 )

                else:
                    pass
                    


