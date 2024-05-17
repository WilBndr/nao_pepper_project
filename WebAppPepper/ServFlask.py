# -*- coding: utf-8 -*-
import webbrowser
from naoqi import ALProxy
from flask import Flask, render_template, redirect, url_for, request, jsonify, Response, session
import socket
from time import sleep
import json
import os
from datetime import timedelta

app = Flask(__name__)
item_index = 0
items_length = 0
app.secret_key = 'votre_clé_secrète'  # Clé secrète pour la session

# Adresse IP du robot Pepper et port
pepper_ip = "11.255.255.100"
pepper_port = 9559

# Connexion aux différents services du robot Pepper
try:
    tablet_service = ALProxy("ALTabletService", pepper_ip, pepper_port)
    autonomous_life_proxy = ALProxy("ALAutonomousLife", pepper_ip, pepper_port)
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


@app.before_first_request
def before_first_request():
    session['logged_in'] = False
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)  # Durée de la session

@app.route('/startQuiz', methods=['GET','POST'])
def start_quiz():
    if request.method == 'POST':
        #animated_speech_proxy.say("\\rspd=100\\Bonjour! Merci de participer au quiz.")
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

@app.route('/adminLog', methods=['GET','POST'])
def login_page():
    return render_template('login.html')


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
    string_value = current_presentation_item[get_index()].get('value').encode('utf-8')
    animated_speech_proxy.say(string_value)
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
    string_value = current_presentation_item[get_index()-1].get('vrai').encode('utf-8')
    animated_speech_proxy.say(string_value)
    #on doit faire -1 car l'index est incrémenté avant l'appel de la fonction
    print(current_presentation_item[get_index()-1].get('vrai'))
    return Response(status=204)
    
    
@app.route('/wrongAnswer', methods=['GET','POST'])
def false_button():
    current_presentation_item = get_current_presentation_item()
    string_value = current_presentation_item[get_index()-1].get('faux').encode('utf-8')
    animated_speech_proxy.say(string_value)
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
                # Suppression de l'élément de la liste pour que le nom ne soit pas ajouté au contenu de la présentation
                content_data.remove(content_item)
                break
        
        if not presentation_name:
            return jsonify({'error': 'Nom de présentation non spécifié'}), 400
        
        # Vérifier si le fichier existe déjà
        file_path = 'content_data.json'
        presentations = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                presentations = json.load(file)
        
        # Récupérer et conserver la présentation actuelle si elle existe
        current_presentation = presentations.get('current_presentation', None)

        # Vérifier si le nom de la présentation existe déjà
        existing_presentation = None
        for existing in presentations.get('presentations', []):
            if existing['name'] == presentation_name:
                existing_presentation = existing
                break
        
        # Si la présentation existe, ajouter le contenu à cette présentation
        if existing_presentation:
            existing_presentation['content'] += content_data
        else:
            # Sinon, créer une nouvelle présentation
            new_presentation = {"name": presentation_name, "content": content_data}
            presentations.setdefault('presentations', []).append(new_presentation)

        # Réinsérer la présentation actuelle dans les données
        if current_presentation:
            presentations['current_presentation'] = current_presentation
        
        # Enregistrer les données dans le fichier JSON
        with open(file_path, 'w') as file:
            json.dump(presentations, file, indent=4)
        
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

def handle_webview_error(error):
    # Gérer l'erreur de chargement de la page web, par exemple en l'enregistrant dans un fichier journal
    with open("webview_errors.log", "a") as log_file:
        log_file.write("Error loading webview: %s" % (error))

# Charger la page web dans une WebView sur la tablette de Pepper
def load_webview():
    print("Chargement de la page web dans une WebView sur la tablette de Pepper")
    try:
        tablet_service.showWebview("http://%s:%d" % (adresse_ip, port))
    except Exception as e:
        handle_webview_error(str(e))

# Passer Pepper en mode Autonomous Life
def set_autonomous_life():
    try:
        # Mettre Pepper en mode Autonomous Life
        autonomous_life_proxy.setState("disabled")
        print("Pepper est maintenant en mode Autonomous Life (interactif).")
    except Exception as e:
        print("Erreur lors du passage en mode Autonomous Life:", e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vérification des informations d'identification
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin_page'))
    return render_template('login.html')

@app.route('/adminPage', methods=['GET', 'POST'])
def admin_page():
    if 'logged_in' in session and session['logged_in']:
        return render_template('adminPage.html')
    else:
        return redirect(url_for('login'))

# Lancement du serveur Flask
if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    adresse_ip = socket.gethostbyname(socket.gethostname())
    print("Adresse IP : %s" % adresse_ip)

    # Définition du port pour le serveur Flask
    port = 5000

    print("Port : %d" % port)

    # Charger la page web dans une WebView sur la tablette de Pepper
    #set_autonomous_life()

    #load_webview()

    #ouvrir le navigateur
    webbrowser.open('http://%s:%d' % (adresse_ip, port))

    # Lancement du serveur Flask
    app.run(host=adresse_ip, port=port)

    
    
    
