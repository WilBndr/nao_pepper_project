# -*- coding: utf-8 -*-
from naoqi import ALProxy
from flask import Flask, render_template, redirect, url_for, request
import socket

app = Flask(__name__)

# Adresse IP du robot Pepper et port
pepper_ip = "11.0.0.108"
pepper_port = 9559

# Connexion aux différents services du robot Pepper
try:
    tablet_service = ALProxy("ALTabletService", pepper_ip, pepper_port)
    motion_proxy = ALProxy("ALMotion", pepper_ip, pepper_port)
    behavior_manager = ALProxy("ALBehaviorManager", pepper_ip, pepper_port)
    tts_proxy = ALProxy("ALTextToSpeech", pepper_ip, pepper_port)
    posture_proxy = ALProxy("ALRobotPosture", pepper_ip, pepper_port)
    audio_device_proxy = ALProxy("ALAudioDevice", pepper_ip, pepper_port)
    animated_speech_proxy = ALProxy("ALAnimatedSpeech", pepper_ip, pepper_port)
except Exception as e:
    print("Erreur lors de la connexion au robot Pepper:", e)

# Changer la langue du robot en français
tts_proxy.setLanguage("French")

@app.route('/startQuiz', methods=['GET','POST'])
def start_quiz():
    if request.method == 'POST':
        animated_speech_proxy.say("\\rspd=100\\Bonjour! Merci de participer au quiz.")
        return render_template('index.html')
    else:
        return render_template('startQuiz.html')

@app.route('/')
def index_page():
    # Rediriger vers la page startQuiz
    return redirect(url_for('start_quiz'))

# Fonction pour charger la page web dans une WebView sur la tablette de Pepper
def load_webview():
    tablet_service.showWebview("http://%s:%d" % (adresse_ip, port))

# Lancement du serveur Flask
if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    adresse_ip = socket.gethostbyname(socket.gethostname())
    print("Adresse IP : %s" % adresse_ip)

    # Définition du port pour le serveur Flask
    port = 5000  # Par défaut, utilisez un autre port si nécessaire

    print("Port : %d" % port)

    # Charger la page web dans une WebView sur la tablette de Pepper
    load_webview()

    # Lancement du serveur Flask
    app.run(host=adresse_ip, port=port)
