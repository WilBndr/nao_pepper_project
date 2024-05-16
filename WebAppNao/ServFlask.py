# -*- coding: utf-8 -*-
from datetime import timedelta
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session
import socket
from naoqi import ALProxy

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'  # Clé secrète pour la session

# Adresse IP du robot NAO et port
nao_ip = "nao.local."
nao_port = 9559

# Connexion aux différents services du robot NAO
try:
    motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
    behavior_manager = ALProxy("ALBehaviorManager", nao_ip, nao_port)
    tts_proxy = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    posture_proxy = ALProxy("ALRobotPosture", nao_ip, nao_port)
    audio_device_proxy = ALProxy("ALAudioDevice", nao_ip, nao_port)
except Exception as e:
    print("Erreur lors de la connexion au robot NAO:", e)

@app.before_first_request
def before_first_request():
    session['logged_in'] = False
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)  # Durée de la session


installed_behaviors = behavior_manager.getInstalledBehaviors()

# Affichage de la liste des comportements installés

print("Liste des comportements installés sur le robot NAO :")
for behavior_info in installed_behaviors:
    print("- {}".format(behavior_info))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vérification des informations d'identification
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('index_page'))
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
def index_page():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/move_forward', methods=['POST'])
def move_forward():
    # Envoyer la commande au robot NAO pour avancer
    motion_proxy.moveToward(0.5, 0, 0)
    return redirect(url_for('index_page'))

@app.route('/move_backward', methods=['POST'])
def move_backward():
    # Envoyer la commande au robot NAO pour reculer
    motion_proxy.moveToward(-0.5, 0, 0)
    return redirect(url_for('index_page'))

@app.route('/say_hello', methods=['POST'])
def say_hello():
    # Envoyer la commande au robot NAO pour dire "Hello, world!"
    tts_proxy.say("Hello, world!")
    return redirect(url_for('index_page'))

@app.route('/start_baby_shark_dance', methods=['POST'])
def start_baby_shark_dance():
    # Réduire le volume au minimum
    audio_device_proxy.setOutputVolume(0)
    # Démarrer l'application "BabySharkDance"
    try:
        behavior_manager.runBehavior("baby_shark_dance-566cf7/behavior_1")
        print("Application BabySharkDance lancée avec succès.")
    except Exception as e:
        print("Erreur lors du lancement de l'application BabySharkDance:", e)
    return redirect(url_for('index_page'))

@app.route('/start_odysseo_presentation', methods=['POST'])
def start_odysseo_presentation():
    # Démarrer l'application "BabySharkDance"
    try:
        behavior_manager.runBehavior("welcome-odysseo/behavior_1")
        print("Application lancée avec succès.")
    except Exception as e:
        print("Erreur lors du lancement de l'application BabySharkDance:", e)
    return redirect(url_for('index_page'))

@app.route('/stop_action', methods=['POST'])
def stop_action():
    # Arrêter toutes les actions en cours sur le robot NAO
    try:
        motion_proxy.stopMove()
        behavior_manager.stopAllBehaviors()
        tts_proxy.stopAll()
        posture_proxy.goToPosture("StandInit", 0.5)  # Réglez la vitesse à 50%
        print("Toutes les actions ont été arrêtées et le robot est en position StandInit.")
    except Exception as e:
        print("Erreur lors de l'arrêt des actions:", e)
    return redirect(url_for('index_page'))

@app.route('/change_volume', methods=['POST'])
def change_volume():
    # Récupérer la valeur du volume à partir de la requête POST
    volume = int(request.form['volume'])
    # Modifier le volume du robot NAO
    try:
        audio_device_proxy.setOutputVolume(volume)
        print("Volume modifié avec succès.")
    except Exception as e:
        print("Erreur lors de la modification du volume:", e)
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    adresse_ip = socket.gethostbyname(socket.gethostname())
    print("Adresse IP : %s" % adresse_ip)

    # Définition du port pour le serveur Flask
    port = 5000  # Par défaut, utilisez un autre port si nécessaire

    print("Port : %d" % port)
    webbrowser.open("http://%s:%d" % (adresse_ip, port))

    # Lancement du serveur Flask
    app.run(host=adresse_ip, port=port)
