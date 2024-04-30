from flask import Flask, render_template, request, redirect, url_for
import socket

app = Flask(__name__)

# Variable globale pour stocker l'index
index = 0

@app.route('/')
def index_page():
    # Renvoyer le modèle HTML avec l'index actuel
    return render_template('index.html', current_index=index)

@app.route('/increment_index', methods=['POST'])
def increment_index():
    global index
    # Incrémenter l'index à chaque fois que le bouton est cliqué
    index += 1
    print("Button clicked! Current index:", index)
    # Rediriger vers la page d'accueil après le clic sur le bouton
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    # Obtention de l'adresse IP de l'ordinateur
    hostname = socket.gethostname()
    adresse_ip = socket.gethostbyname(hostname)
    print(f"Adresse IP : {adresse_ip}")

    # Définition du port pour le serveur Flask
    port = 5000  # Par défaut, utilisez un autre port si nécessaire

    print(f"Port : {port}")

    # Lancement du serveur Flask
    app.run(host='0.0.0.0', port=port)
