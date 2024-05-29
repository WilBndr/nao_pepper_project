# -*- coding: utf-8 -*-
from datetime import timedelta
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import socket
import json
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
    battery_proxy = ALProxy("ALBattery", nao_ip, nao_port)
except Exception as e:
    print("Erreur lors de la connexion au robot NAO:", e)

@app.before_first_request
def before_first_request():
    session['logged_in'] = False
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)  # Durée de la session


#installed_behaviors = behavior_manager.getInstalledBehaviors()

#posture_proxy.getPostureList()  # Affichage de la liste des postures installées

# Affichage de la liste des comportements installés

'''
print("Liste des comportements installés sur le robot NAO :")
for behavior_info in installed_behaviors:
    print("- {}".format(behavior_info))
'''



@app.route('/battery_level')
def battery_level():
    # Obtenir le niveau de la batterie du robot NAO
    
    battery_level = battery_proxy.getBatteryCharge()

    # Convertir le dictionnaire en JSON en utilisant json.dumps
    return json.dumps({'battery_level': battery_level})

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


@app.route('/', methods=['GET', 'POST'])
def index_page():

    if request.method == 'POST':

        stop_running_behaviors()

        data = request.get_json()
        action = data.get('action')
        print("Action:", action)
        
        if action == 'start_behavior':
                if "requinspresentation" in data.get('behavior'):
                    tts_proxy.setLanguage("French")
                    print("Langue: Français")
                else:
                    tts_proxy.setLanguage("English")
                    print("Langue: anglais")
                behavior_name = data.get('behavior')
                print("Behavior name:", behavior_name)
                behavior_manager.runBehavior(str(behavior_name))
                return jsonify({}), 204
        elif action == 'go_posture':
            posture_name = data.get('posture')
            posture_proxy.goToPosture(str(posture_name), 0.5)  # Réglez la vitesse à 50%
            return jsonify({}), 204
        elif action == 'set_volume':
            volume = data.get('volume')
            audio_device_proxy.setOutputVolume(int(volume))
            return jsonify({}), 204
        elif action == 'move':
            x = data.get('x')
            y = data.get('y')
            theta = data.get('theta')
            motion_proxy.moveToward(x, y, theta)
            return jsonify({}), 204
        elif action == 'stop_move':
            motion_proxy.stopMove()
            behavior_manager.stopAllBehaviors()
            tts_proxy.stopAll()
            posture_proxy.goToPosture("Stand", 0.5)
            return jsonify({}), 204
        else:
            return jsonify({'error': 'Invalid request'}), 400

    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

def stop_running_behaviors():
    # Arrêter tous les comportements en cours
    try:
        running_behaviors = behavior_manager.getRunningBehaviors()
        for behavior in running_behaviors:
            behavior_manager.stopBehavior(behavior)
    except Exception as e:
        print("Erreur lors de l'arrêt des comportements en cours:", e)  

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
