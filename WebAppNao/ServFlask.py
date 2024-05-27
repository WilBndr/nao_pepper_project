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


installed_behaviors = behavior_manager.getInstalledBehaviors()

# Affichage de la liste des comportements installés


print("Liste des comportements installés sur le robot NAO :")
for behavior_info in installed_behaviors:
    print("- {}".format(behavior_info))


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

        print("POST request received.")
        data = request.get_json()
        action = data.get('action')
        print("Action:", action)
        if action == 'start_behavior':
                behavior_name = data.get('behavior')
                print("Behavior name:", behavior_name)
                behavior_manager.runBehavior(str(behavior_name))
                return jsonify({}), 204
        else:
            return jsonify({'error': 'Invalid request'}), 400
    

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

    stop_running_behaviors()
    
    # Démarrer l'application "BabySharkDance"
    try:
        behavior_manager.runBehavior("baby_shark_dance-566cf7/behavior_1")
        print("Application BabySharkDance lancée avec succès.")
    except Exception as e:
        print("Erreur lors du lancement de l'application BabySharkDance:", e)

    return redirect(url_for('index_page'))

@app.route('/start_odysseo_presentation', methods=['POST'])
def start_odysseo_presentation():

    stop_running_behaviors()

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

@app.route('/me_fr_action', methods=['POST'])
def me_fr_action():

    stop_running_behaviors()

    # Arrêter toutes les actions en cours sur le robot NAO
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/RaiseArm")
        print("Application lancée avec succès.")
    except Exception as e:
        print("Erreur lors du lancement de l'application BabySharkDance:", e)
        
    return render_template('index.html')

@app.route('/fear_fr_action', methods=['POST'])
def fear_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/FearSharks")
        print("Comportement de peur lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement de peur:", e)
    return jsonify({}), 204

@app.route('/notConviced_fr_action', methods=['POST'])
def notConviced_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Thinking")
        print("Comportement pas convaincu lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement pas convaincu:", e)
    return jsonify({}), 204

@app.route('/sharkFish_fr_action', methods=['POST'])
def sharkFish_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/InteruptOpenArms")
        print("Comportement poissons requin lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement poissons requin:", e)
    return jsonify({}), 204

@app.route('/ears_fr_action', methods=['POST'])
def ears_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/TouchingEars")
        print("Comportement touche ses oreilles lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement touche ses oreilles:", e)
    return jsonify({}), 204

@app.route('/lookAtAquarium_fr_action', methods=['POST'])
def lookAtAquarium_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/turnBothSides")
        print("Comportement regarde aquarium lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement regarde aquarium:", e)
    return jsonify({}), 204

@app.route('/unbelievable_fr_action', methods=['POST'])
def unbelievable_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Exclamation")
        print("Comportement c'est pas vrai lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement c'est pas vrai:", e)
    return jsonify({}), 204

@app.route('/weAreSharks_fr_action', methods=['POST'])
def weAreSharks_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/WeAreSharks")
        print("Comportement nous sommes des requins lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement nous sommes des requins:", e)
    return jsonify({}), 204

@app.route('/no_fr_action', methods=['POST'])
def no_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/No")
        print("Comportement non lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement non:", e)
    return jsonify({}), 204

@app.route('/IWant_fr_action', methods=['POST'])
def IWant_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Excited")
        print("Comportement oui je veux lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement oui je veux:", e)
    return jsonify({}), 204

@app.route('/interest_fr_action', methods=['POST'])
def interest_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Interst_about_sharks")
        print("Comportement requin intéressant lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement requin intéressant:", e)
    return jsonify({}), 204

@app.route('/AskVisitors_fr_action', methods=['POST'])
def AskVisitors_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/AskToVisitors")
        print("Comportement demande aux visiteurs lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement demande aux visiteurs:", e)
    return jsonify({}), 204

@app.route('/BodyBuilding_fr_action', methods=['POST'])
def BodyBuilding_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/BodyBuilding_Pose")
        print("Comportement bodybuilding lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement bodybuilding:", e)
    return jsonify({}), 204

@app.route('/IKnow_fr_action', methods=['POST'])
def IKnow_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Nao_Knows")
        print("Comportement je sais lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement je sais:", e)
    return jsonify({}), 204

@app.route('/ProtectSharks_fr_action', methods=['POST'])
def ProtectSharks_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Why_protect_sharks")
        print("Comportement comment protéger les requins lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement comment protéger les requins:", e)
    return jsonify({}), 204

@app.route('/LikeSharks_fr_action', methods=['POST'])
def LikeSharks_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/Feels_good_about_sharks")
        print("Comportement j'aime les requins lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement j'aime les requins:", e)
    return jsonify({}), 204

@app.route('/SharkDancePropose_fr_action', methods=['POST'])
def SharkDancePropose_fr_action():
    stop_running_behaviors()
    try:
        behavior_manager.runBehavior("sharkpresentation-b89c11/bby_shark_propose")
        print("Comportement danse du requin propositions lancé avec succès.")
    except Exception as e:
        print("Erreur lors du lancement du comportement danse du requin propositions:", e)
    return jsonify({}), 204


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
