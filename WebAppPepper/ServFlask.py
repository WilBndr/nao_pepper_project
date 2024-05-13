# -*- coding: utf-8 -*-
import webbrowser
from naoqi import ALProxy
from flask import Flask, render_template, redirect, url_for, request, jsonify
import socket
from time import sleep
import json

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
#tts_proxy.setLanguage("French")

@app.route('/startQuiz', methods=['GET','POST'])
def start_quiz():
    if request.method == 'POST':
        animated_speech_proxy.say("\\rspd=100\\Bonjour! Merci de participer au quiz.")
        # Mettre en pause l'exécution pendant 3 secondes
        sleep(1)
        # Rediriger vers la page question.html
        return redirect(url_for('question_page'))
    else:
        return render_template('startQuiz.html')
    
@app.route('/configPage', methods=['GET','POST'])
def config_page():
    return render_template('configPage.html')

import json

@app.route('/submitContent', methods=['POST'])
def submit_content():
    if request.method == 'POST':
        content_data = request.json
        # Traitement des données reçues
        with open('content_data.json', 'w') as file:
            data_to_save = {"presentations": []}
            presentation_index = 1
            content_index = 1
            current_presentation = {"name": "Présentation {}".format(presentation_index), "content": []}
            for content_item in content_data:
                if content_item['type'] == 'question':
                    # Si le type est une question, enregistrez également les réponses vraies et fausses
                    question = content_item['value']
                    vrai = content_item['vrai']
                    faux = content_item['faux']
                    current_presentation["content"].append({
                        "type": "question",
                        "index": content_index,
                        "question": question,
                        "vrai": vrai,
                        "faux": faux
                    })
                else:
                    current_presentation["content"].append({
                        "type": "paragraphe",
                        "index": content_index,
                        "value": content_item['value']
                    })
                content_index += 1
            data_to_save["presentations"].append(current_presentation)
            json.dump(data_to_save, file, indent=4)
        return jsonify({'message': 'Données enregistrées avec succès'}), 200
    else:
        return jsonify({'error': 'Méthode non autorisée'}), 405

@app.route('/')
def index_page():
    # Rediriger vers la page startQuiz
    return redirect(url_for('start_quiz'))

@app.route('/question')
def question_page():
    return render_template('question.html')

# Fonction pour charger la page web dans une WebView sur la tablette de Pepper
def load_webview():
    tablet_service.showWebview("http://%s:%d" % (adresse_ip, port))

# Lancement du serveur Flask
if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    adresse_ip = socket.gethostbyname(socket.gethostname())
    print("Adresse IP : %s" % adresse_ip)

    # Définition du port pour le serveur Flask
    port = 5000

    print("Port : %d" % port)

    # Charger la page web dans une WebView sur la tablette de Pepper
    #load_webview()

    #ouvrir le navigateur
    webbrowser.open('http://%s:%d' % (adresse_ip, port))

    # Lancement du serveur Flask
    app.run(host=adresse_ip, port=port)

    #ouvrir le navigateur
