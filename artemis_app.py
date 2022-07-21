import psutil
import sys, getopt
import signal
import time
import csv
from edge_impulse_linux.audio import AudioImpulseRunner


from scipy.io.wavfile import write
from os.path import exists
from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import subprocess
import json
import numpy as np

from io import BytesIO

from lightControl.phue import lightsController
from record import recognize
from IPython.display import Audio, display

with open ("command/command.json", "r") as f:
    command = json.load(f)


runner = None

def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def help():
    print('python classify.py <path_to_model.eim> <audio_device_ID, optional>' )

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) == 0:
        help()
        sys.exit(2)

    model = args[0]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        restart = True
        i=0
        while restart:
            try:
                model_info = runner.init()
                labels = model_info['model_parameters']['labels']
                print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

                selected_device_id = None
                if len(args) >= 2:
                    selected_device_id=int(args[1])
                    print("Device ID "+ str(selected_device_id) + " has been provided as an argument.")
                
                for res, audio in runner.classifier(device_id=selected_device_id):

                    restart=False
                    for label in labels:
                        #Change ['okartemis'] to your own classification name that you've set in edge-impusle
                        score = res['result']['classification']['okartemis']
                        
                        
                        if score >=0.98:
                            #loop to avoid calling recognize() multiple times
                            if i == 0:    
                                
                                print('reccording')
                                time.sleep(0.2)
                                recognize()
                                restart = True
                                i+=1
                                break
                            if i >= 1 and i <= 10:
                                i += 1
                            elif i > 10:
                                i=0

            finally:
                if (runner):
                    runner.stop()

if __name__ == '__main__':
    main(sys.argv[1:])
