## :construction: En construction :construction:

# **Artemis**: petit assistant vocal en français

Cette application est un exemple d'assistant vocal qui peut être embarqué sur un Raspberry Pi 4. 
Etant donné l'utilisation de Tensorflow est Spacy et les incompatibilités notables sur bulleyes 32 bit et python 3.9 cela fonctionne uniquement sous linux **aarch64**

Un environnement virtuel (avec pyenv par ex) sera plus sûr pour ce petit projet :wink:.  

## Hardware:

- Raspberry Pi (RPi 4 8G de préférence)
- Carte SD avec Bulleyes 64 bit pré-installé (aarch64)
- Un microphone usb (type dongle peux faire l'affaire)
- Ventilateur 5v 
- Haut parleur usb

## Wake Word
Le "WakeWord" ou "mot de réveil" est similaire à "Alexa" ou "Ok Google". Ici j'ai choisi "Ok Artemis". Bien qu'il existe d'autres solutions, j'ai choisi d'utiliser l'api [Edge-impulse](https://www.edgeimpulse.com/ "Edge impulse"). Après la création d'un compte (gratuit) il suffit de se laisser porter par la doc.
La création du modèle est relativement simple en suivant la doc et le [tutoriel](https://www.youtube.com/watch?v=vbIg4Up1Ts0&ab_channel=EdgeImpulse "tutoriel") qui sont bien expliquée. La seule contrainte est qu'il est impératif d'entrainer le model avec un très grand nombre d'échantillons. Dans l'idéal il faut une 20aine de minutes d'enregistrements d'une seconde contenant le "mot de réveil", prononcé par différentes personnes avec diverses intonations pour rendre le model plus fiable et ainsi éviter les faux postifs. Si une seule voix entraine le model, alors seulement cette voix sera reconnue. Il faut aussi autant d'enregistrement de "bruit de fond" mais aussi "d'inconnus". Edge impulse se charge de spliter equitablement le dataset (train vs test). Il y aura donc trois classes en sortie de model. 
Une fois le modèle entrainé, il faut installer l'api edge-impule-linux et télécharger le modèle.

`curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
npm config set user root && sudo npm install edge-impulse-linux -g --unsafe-perm`

Initialiser edge-impulse-linux avec ses identifiants

`edge-impulse-linux --disable-camera` # l'argument disable-camera est nécessaire puisque seul "keyword spoting" est utilisé

installer les dépendances manquantes

`sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev`

`pip3 install edge_impulse_linux -i https://pypi.python.org/simple`

Telecharger le modèle

`edge-impulse-linux-runner --download modelfile.eim`

## Dépendances


### installation de Vosk (speech to text):

`python3 -m pip install https://github.com/alphacep/vosk-api/releases/download/0.3.21/vosk-0.3.21-py3-none-linux_aarch64.whl`

Afin de faire fonctionner Vosk il est nécessaire de télécharger le modèle fr small (41 Mb) depuis le site [alphacephei.com](https://alphacephei.com/vosk/models "alphacephei.com"). Apres avoir décompréssé le fichier, il faut de renommer le dossier contenant le modèle ("vosk-model-small-fr-0.22" => "VoskModel") et le placer à la racine.
Un model plus lourd sera plus efficace mais aussi beaucoup plus long à charger à chaque lancement du script artemis_app.py.

### Installer Spacy:
Ce package permet de faire de l'analyse sémantique et il est relativement poussé et complexe. Nous l'utiliserons ici uniquement comme lemmatizer, car nltk ne prend pas en charge le français.

:warning: Spacy fonctionne uniquement sur la version 64 bit du raspberry pi. :warning:

`pip install spacy`

Installer le model spacy fr

`python -m spacy download fr_core_news_md`

### Installer Tensorflow sur raspberrypi 64bit pour python 3.9:

Une procédure plutot facile à suivre [ici](https://qengineering.eu/install-tensorflow-2.7-on-raspberry-64-os.html "ici")

### Controller les lumières: exemple avec philips Hue:
le package phue 1.1 permet de se connecter au pont philips hue afin de récuprer les infos (scenes, groupes, zones etc ...)

la doc est bien faite et est disponible [ici](https://github.com/studioimaginaire/phue)

`pip install phue`

Il est ensuite nécessaire de modifier le fichier /command/command.json afin d'y ajouter les commandes souhaitées et les actions qui correspondent à vos propres zones/groupes/scenes etc...

### gTTS (google text to speech)

Un package ne nécessitant pas de faire appel à une api tierce aurait été préférable, mais la plupart des synthétizeur vocaux (ex : pyttsx3) ressemble malheureusement à des larynx électroniques de très mauvaise qualité.

### intents:
Artemis peut aussi être considérer comme un chatbot. Je me suis basé sur plusieurs tutoriels (comme [ici](https://www.youtube.com/watch?v=1lwddP0KUEg), ou encore [ici](https://towardsdatascience.com/how-to-create-a-chatbot-with-python-deep-learning-in-less-than-an-hour-56a063bdfc44)).
Le fichier intents.json (ArtemisAi/response_artemis) contient les différentes questions/reponses qu'Artemis est capable de gérer. On peut ajouter autant d'objets qu'on le souhaite, mais il est impératif d'entrainer le model après toutes modifications.

`python training.py`

## :rocket: Lancer Artemis :rocket:
Une fois les dépendences installées il suffit de lancer le script python avec le nom du model (".eim") comme argument ainsi que l'index de la carte du micro. Si aucun index est rentré comme second argument, une liste apparaitra, permettant de selectionner le micro usb qui est connecté.
Il est préférable de choisir l'index correspondant à **"default"**.

`python artemis_app.py modelfile.eim`

Et voila...


