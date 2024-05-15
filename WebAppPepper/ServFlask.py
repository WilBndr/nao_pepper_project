# -*- coding: utf-8 -*-
import webbrowser
from naoqi import ALProxy
from flask import Flask, render_template, redirect, url_for, request, jsonify, Response
import socket
from time import sleep
import json
import os

app = Flask(__name__)
item_index = 0
items_length = 0

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

@app.route('/choosePage', methods=['GET','POST'])
def choose_presentation():
    # Charger les données depuis le fichier JSON
    with open('content_data.json', 'r') as file:
        data = json.load(file)
        presentations = data.get('presentations', [])

    # Rendre le modèle HTML en incluant les données des présentations
    return render_template('presentationPage.html', presentations=presentations)

@app.route('/selectPresentation', methods=['POST'])
def select_presentation():
    if request.method == 'POST':
        # Récupérer le nom de la présentation sélectionnée à partir des données du formulaire
        selected_presentation = request.form.get('selectedPresentation')
        
        # Vérifier si le fichier existe déjà
        file_path = 'content_data.json'
        if os.path.exists(file_path):
            # Charger les données du fichier JSON
            with open(file_path, 'r') as file:
                data_to_save = json.load(file)
                
                # Vérifier si le champ current_presentation existe déjà
                if 'current_presentation' in data_to_save:
                    # Mettre à jour le champ current_presentation avec la nouvelle valeur
                    data_to_save['current_presentation'] = selected_presentation
                else:
                    # Créer le champ current_presentation avec la nouvelle valeur
                    data_to_save['current_presentation'] = selected_presentation
                
                # Enregistrer les données mises à jour dans le fichier JSON
                with open(file_path, 'w') as file:
                    json.dump(data_to_save, file, indent=4)

                return index_page()
        else:
            return jsonify({'error': 'Fichier de données introuvable'}), 404
    else:
        return jsonify({'error': 'Méthode non autorisée'}), 405


@app.route('/startPresentation', methods=['POST'])
def start_presentation():

    robot_current_speach()

    return render_template('question.html', current_presentation_item=get_current_presentation_item())

def robot_current_speach():
    current_presentation_item = get_current_presentation_item()
    #animated_speech_proxy.say(current_presentation_item[get_index()].get('value'))
    print(current_presentation_item[get_index()].get('value'))
    print(get_index())
    print(get_length())
    increment_index()

@app.route('/nextButton', methods=['GET','POST'])
def next_button():
    if get_index() < get_length():
        robot_current_speach()
        return Response(status=204)
    else:
        #on reset l'index de manière a poivoir relancer la présentation
        reset_index()
        return render_template('endQuiz.html')
    
@app.route('/trueAnswer', methods=['GET','POST'])
def true_button():
    current_presentation_item = get_current_presentation_item()
    #animated_speech_proxy.say(current_presentation_item[get_index()].get('value'))
    #on doit faire -1 car l'index est incrémenté avant l'appel de la fonction
    print(current_presentation_item[get_index()-1].get('vrai'))
    return Response(status=204)
    
    
@app.route('/wrongAnswer', methods=['GET','POST'])
def false_button():
    current_presentation_item = get_current_presentation_item()
    #animated_speech_proxy.say(current_presentation_item[get_index()].get('value'))
    print(current_presentation_item[get_index()-1].get('faux'))
    return Response(status=204)
    
def increment_index():
    global item_index
    item_index += 1

def get_index():
    return item_index

def get_length():
    global items_length
    items_length = len(get_current_presentation_item())
    return items_length

def reset_index():
    global item_index
    item_index = 0

def get_current_presentation_item():

    with open('content_data.json', 'r') as file:
        data = json.load(file)
        presentations = data.get('presentations', [])
        current_presentation_name = data.get('current_presentation', '')
    
    current_presentation_item = []

    for presentation in presentations:
        if presentation['name'] == current_presentation_name:
            for content_item in presentation['content']:
                current_presentation_item.append(content_item)
            break

    return current_presentation_item

@app.route('/submitContent', methods=['POST'])
def submit_content():
    if request.method == 'POST':
        content_data = request.json
        presentation_name = None
        for content_item in content_data:
            if content_item['type'] == 'presentationName':
                presentation_name = content_item['value']
                #suppression de l'élément de la liste pour que le nom ne soit pas ajouté au contenu de la présentation
                content_data.remove(content_item)
                break
        
        if not presentation_name:
            return jsonify({'error': 'Nom de présentation non spécifié'}), 400
        
        # Vérifier si le fichier existe déjà
        file_path = 'content_data.json'
        presentations = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                presentations = json.load(file).get('presentations', [])
        
        # Vérifier si le nom de la présentation existe déjà
        existing_presentation = None
        for existing in presentations:
            if existing['name'] == presentation_name:
                existing_presentation = existing
                break
        
        # Si la présentation existe, ajouter le contenu à cette présentation
        if existing_presentation:
            existing_presentation['content'] += content_data
        else:
            # Sinon, créer une nouvelle présentation
            new_presentation = {"name": presentation_name, "content": content_data}
            presentations.append(new_presentation)
        
        # Enregistrer les données dans le fichier JSON
        with open(file_path, 'w') as file:
            json.dump({"presentations": presentations}, file, indent=4)
        
        return jsonify({'message': 'Données enregistrées avec succès'}), 200
    else:
        return jsonify({'error': 'Méthode non autorisée'}), 405

def get_current_presentation():
    # Charger les données depuis le fichier JSON
    with open('content_data.json', 'r') as file:
        data = json.load(file)
        current_presentation = data.get('current_presentation', '')
    
    return current_presentation

@app.route('/endQuiz')
def end_quiz():
    return render_template('endQuiz.html')

@app.route('/returnMenu', methods=['GET','POST'])
def return_menu():
    return render_template('startQuiz.html',current_presentation=get_current_presentation())

@app.route('/')
def index_page():
    # Rediriger vers la page startQuizs
    return render_template('startQuiz.html',current_presentation=get_current_presentation())

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
