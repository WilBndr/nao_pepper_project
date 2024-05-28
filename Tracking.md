# Tracking NAO_PEPPER_Project

## Points abordés lors de notre entrevue avec Dr. Shaad Ally Toofanee

### 1. Travail avec une ONG (Century) pour les enfants handicapés (NAO)
- Visite sur place pour comprendre comment aider avec la programmation de nos robots
- Élaboration de scénarios pédagogiques

### 2. Odysseo (NAO)
- Protection de l'environnement marin
- Rendez-vous avec l'aquarium pour discuter de la programmation du robot

### 3. Accueil à l'UDM (NAO)
- Présentation des capacités des robots

## Laboratoire robotique UDM

Après un entretien avec le seul professeur de robotique mauricien enseignant à l'UDM, nous avons appris que le laboratoire avait été créé en 2019 pour pallier un manque de professionnels capables d'effectuer la maintenance des robots présents en entreprise. Celles-ci se trouvaient donc naturellement sceptiques quant à l'idée d'investir en robotique. Ce manque était accentué du fait que l'île est assez éloignée du reste du monde, rendant la venue de techniciens qualifiés coûteuse. L'université a été visionnaire dans sa manière de renforcer et d'accélérer le développement de l'île en démontrant le potentiel des robots et en formant les personnes adéquates pour les entretenir.

## Première phase :

- **Sélection et réflexion sur le projet** - 08/04
- **Recherche de parcours pédagogiques** - 08/04
- **Férié** - 09/04
- **Prise en main du robot** - 10/04
  - Actions possibles :
    - Jouer des audios
    - Parler/Répéter
    - Questionnaires (questions/réponses)
    - Mouvements (25 articulations pour des chorégraphies)
    - Jeu de couleur avec LED (adaptation d'environnement)
    - Travail de sensation (touché, vision, etc.)
    - Autres fonctions de programmation (maths, jeu de données, etc.)
    - Enregistrement de vidéos
    - Différentes langues (20)
    - Animations (emotes)
    - Pepper peut également jouer des vidéos sur son écran

- **Recherche de scénarios pédagogiques** - 10/04
- **Férié** - 11/04
- **Recherche de scénarios pédagogiques** - 12/04
- **Préparation des entretiens avec Century et Odysseo de la semaine prochaine (utilisation de Miro)** - 12/04
- **Recherche sur la faune et les enjeux de l'environnement** - 12/04
- **Finalisation des préparations de l'entretien avec Odysseo, recherches sur les sites internet** - 15/04
- **Recherche sur l'ONG depuis leur site** - 15/04
- **Tests avec le robot (NAO)** - 15/04
- **Réunion avec Odysseo** - 16/04
  - [Compte Rendu](meeting_minutes/meeting_16_04.md)
- **Visite Odysseo** - 16/04
- **Début de l'implémentation de la danse** - 17/04
- **Implémentation de l'ensemble des mouvements de danse** -18/04
- **Test des mouvements de danse en conditions réelles** - 19/04 
  - On a pu observer lors de cette phase de test que le robot perd en équilibre lors de sa danse, cependant en maintenant ses pieds au sol, le robot peut effectuer sa danse sans aucun problème. 
  - Problème lié à l'équilibre (pistes de résolution) : 
    - Réduction de l'amplitude des mouvements
    - Retravailler la position de base du robot pour améliorer l'équilibre
    - Réduction de la vitesse des mouvements et réduction du nombre de mouvements
- **Implémentation de solutions au problème** - 19/04
- **Amélioration globale de la dynamique du robot** - 22/04
- **Test d'affichage sur le second robot** - 22/04
- **Test de la dynamique améliorée concluant pour un mouvement** - 23/04
  - Dynamique à apporter sur les autres robots
- **Test du programme de bienvenue avec Pepper** - 23/04
  - Correction de problèmes logiciels liés à Choregraphe
- **Recherche et mise en place d'un environnement de développement pour déployer une application Kotlin sur la tablette du robot Pepper** - 24/04
  - Alderaban acheté par SoftBank -> app Android plus maintenue et complexe à redévelopper aujourd'hui (versions Windows, version Android Studio, etc.), le plus simple à développer et à déployer est donc une application web

  - Windows 10 nécéssaire au dévellopement d'application Kotlin pour Pepper puisque la virtualisation du robot ne fonctionne que pour cette version du système d'exploitation, windows 11 ne le supporte pas. De plus l'IDE android Studio doit être rétrograddé a sa version bumblebee denière maj en date 2020, il en va de meme pour l'IDE InteliJ de JetBrain.

	- Cette issue est due au fait que les robots développés par Alderaban étaient vendus à un prix élevé, leur principal atout commercial était de pouvoir leur faire faire ce que les entreprises investissant sur ces robots souhaitaient. Ce qui a marché pour NAO puisque le robot était encore abordable, mais cela ne s'est pas reproduit pour Pepper qui était moins accessible. C'est ce qui a amené au rachat d'Alderaban par SoftBank
- **Coordination son/mouvement du robot Pepper** - 24/04
- **Finalisation de la coordination des mouvements de NAO avec le son** - 25/04
 - Vidéo démonstrative de la danse avec NAO
- **Discussion du futur développement réalisé avec Pepper** - 25/04
  - Test de l'utilisation de Pepper (test de reconnaissance vocale, de la tablette tactile ainsi que de la parole)
- **Réception du script réalisé par Odysseo** - 26/04
- **Implémentation du script** - 26/04
- **Mise en place du multilanguages pour le robot** - 29/04
 - On se rend compte que le robot n'est pas a jour (temp d'attente au démarage), installation du francais, connexion en administrateur via un compte alderaban
- **Test application web pour controle distant du robot** - 30/04
 - Nécéssite l'instalation du JDK nao, et de rétrograder python a la version 2.7
- **Finalisation du script fournis par Odysseo** - 30/04
- **Test du script fournis par Odysseo** - 02/05
- **Test de l'application web nao** - 02/05
- **Test mouvements scipt NAO** - 03/05
- **Import de mouvement sur NAO et test sur l'application web** - 06/05
- **Sécurisation de la connexion ave l'application web** - 07/05
- **Implémentation de cas d'usage de la tablette pepper avec l'application web** - 08/05
- **Test d'application web sur la tablette de Pepper** - 08/05
 - En début de projet, je trouvais  l'idée de pouvoir contrôler les actions de Pepper à l'aide de sa tablette assez intéressante. Cependant, avec le logiciel Choregraphe, cette idée est vite devenue inenvisagable à la conception car la suite d'actions était prédéfinie et non modifiable une fois le script lancé. Lorsque je me suis penché sur le développement de l'application web de contrôle distant du robot NAO, l'idée de contrôler Pepper avec sa tablette est devenue bien plus réaliste.

 - Suite à la validation des tests de contrôle à distance du robot NAO, j'ai travaillé sur l'ajout de cette application au robot Pepper. Par chance, la compatibilité du SDK Python pour NAO permettait également de programmer Pepper de la même manière. Il est donc devenu possible de contrôler Pepper depuis sa tablette, ce qui a alors ouvert de nombreuses possibilités. J'ai notamment réalisé un petit quiz animé par Pepper où l'utilisateur devait interagir avec sa tablette pour montrer cette fonctionnalité. Après m'être entretenu avec Dr. Shaad pour lui faire part de mes avancées, nous avons convenu qu'il serait désormais nécessaire aux futurs utilisateurs de pouvoir réaliser eux-mêmes leurs propres quiz et que l'utilisation du robot devienne accessible à tous.
- **Présentation des robots aux METC à Pailles (Mauritius Emerging technologies Council)** - 09/05
- **Présentation des robots aux METC à Pailles (Mauritius Emerging technologies Council)** - 10/05
- **Présentation des robots aux METC à Pailles (Mauritius Emerging technologies Council)** - 11/05
- **Implémentation de la rédaction de présentation pour Pepper via l'application web** - 13/05
- **Implémentation de la sauvegarde de présentation pour Pepper via l'application web** - 14/05
- **Implémentation du passage de présentation pour Pepper via l'application web** - 15/05
- **Présentation mis parcour et test des script avant présentation pour Odysseo, conffiguration des presentation sur pepper** - 16/05
- **Documentation installation de l'environnement pour applications robots** - 17/05
- **Tests sur application de Pepper** - 17/05
- **Réaisation de la vidéo de présentation de l'application pour Pepper** - 20/05
- **Préparation de la démo pour Odysseo** - 20/05
- **Avancement sur le rapport de stage** - 21/05
- **Finalisation du guide d'installation** - 21/05
- **Présentation de l'avancé du projet à Odysseo** 22/05
- **Implémentation du dernier script fournis par Odysseo** - 23/05
- **Mise à jour de l'application web ppur incorporer le nouveau script** - 24/05
- **Correction de bug de l'appli web ajout de l'utilisation de ajax** - 27/25
- **Réalisation du script en anglais** - 28/05