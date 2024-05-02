# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import socket
from naoqi import ALProxy

app = Flask(__name__)




# Adresse IP du robot NAO et port
nao_ip = "11.0.0.101"  # À remplacer par l'adresse IP réelle de votre robot NAO
nao_port = 9559

# Adresse IP du robot NAO et port
# nao_ip = "127.0.0.1"  # À remplacer par l'adresse IP réelle de votre robot NAO
# nao_port = 9559

tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)

# Connexion au robot NAO
try:
    motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
except Exception as e:
    print("Erreur lors de la connexion au robot NAO:", e)

@app.route('/')
def index_page():
    # Renvoyer le modèle HTML avec l'index actuel
    return render_template('index.html')

@app.route('/move_forward', methods=['POST'])
def move_forward():
    # Envoyer la commande au robot NAO pour avancer
    motion_proxy.moveToward(0.5, 0, 0)
    return redirect(url_for('index_page'))

@app.route('/move_backward', methods=['POST'])
def move_backward():
    # Envoyer la commande au robot NAO pour reculer
    motion_proxy.say("Hello, world!")
    return redirect(url_for('index_page'))

# Ajoutez d'autres routes et fonctions pour d'autres mouvements du robot NAO

@app.route('/say_hello', methods=['POST'])
def say_hello():
    # Envoyer la commande au robot NAO pour reculer
    tts.say("Hello, world!")
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    adresse_ip = socket.gethostbyname(socket.gethostname())
    print("Adresse IP : %s" % adresse_ip)

    # Définition du port pour le serveur Flask
    port = 5000  # Par défaut, utilisez un autre port si nécessaire

    print("Port : %d" % port)

    # Lancement du serveur Flask
    app.run(host=adresse_ip, port=port)
