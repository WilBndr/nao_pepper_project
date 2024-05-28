// Récupérer le curseur de volume
var volumeInput = document.getElementById('volume');

// Vérifier s'il existe une valeur de volume stockée localement
var savedVolume = localStorage.getItem('volume');
if (savedVolume !== null) {
    // Mettre à jour la valeur du curseur de volume
    volumeInput.value = savedVolume;
}

// Écouter les changements de valeur du curseur de volume
volumeInput.addEventListener('input', function() {
    // Stocker la nouvelle valeur du volume localement
    localStorage.setItem('volume', volumeInput.value);
});

// Gestion des boutons Afficher/Cacher
const boutonsAfficher = document.querySelectorAll('.bouton-afficher');
const boutonsCacher = document.querySelectorAll('.bouton-cacher');

boutonsAfficher.forEach(function(boutonAfficher) {
    boutonAfficher.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const contenuAfficher = document.querySelector('.' + targetId);

        contenuAfficher.style.display = 'block';
        this.style.display = 'none';

        // Afficher le bouton Cacher associé
        const boutonCacher = document.querySelector('.bouton-cacher[data-target="' + targetId + '"]');
        boutonCacher.style.display = 'block';
    });
});

boutonsCacher.forEach(function(boutonCacher) {
    boutonCacher.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const contenuAfficher = document.querySelector('.' + targetId);

        contenuAfficher.style.display = 'none';

        // Afficher le bouton Afficher associé
        const boutonAfficher = document.querySelector('.bouton-afficher[data-target="' + targetId + '"]');
        boutonAfficher.style.display = 'block';

        this.style.display = 'none';
    });
});

function updateBatteryLevel() {
    fetch('/battery_level')
        .then(response => response.json())
        .then(data => {
            const batteryLevel = data.battery_level || 0;
            document.getElementById('battery-level').style.width = batteryLevel + '%';
            document.getElementById('battery-text').innerText = batteryLevel;

            // Mettre à jour la classe CSS en fonction du pourcentage de batterie
            const batteryElement = document.getElementById('battery-level');
            batteryElement.className = 'battery-level';

            if (batteryLevel < 20) {
                batteryElement.classList.add('low');
            } else if (batteryLevel < 50) {
                batteryElement.classList.add('medium');
            } else {
                batteryElement.classList.add('high');
            }
        });
}

setInterval(updateBatteryLevel, 20000); // Actualiser toutes les 2 minutes

$(document).ready(function() {

    $("#goForward").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "move", x: 0.5, y: 0, theta: 0}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Action lancée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du lancement de l'action: " + error.responseText);
            }
        });
    });

    $("#goBackward").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "move", x: -0.5, y: 0, theta: 0}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Action lancée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du lancement de l'action: " + error.responseText);
            }
        });
    });
    

    $("#volumeBtn").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "set_volume" , volume: volumeInput.value}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Action stoppée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors de l'arrêt du changement de volume: " + error.responseText);
            }
        });
    });

    $("#stop").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "go_posture", posture: "Stand"}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Action stoppée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors de l'arrêt de l'action: " + error.responseText);
            }
        });
    });

    $("#Stand").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "go_posture", posture: "Stand"}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Posture changée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du changement de posture: " + error.responseText);
            }
        });
    });

    $("#Sit").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "go_posture", posture: "Sit"}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Posture changée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du changement de posture: " + error.responseText);
            }
        });
    });

    $("#LyingBack").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "go_posture", posture: "LyingBack"}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Posture changée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du changement de posture: " + error.responseText);
            }
        });
    });

    $("#LyingBelly").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "go_posture", posture: "LyingBelly"}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Posture changée: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du changement de posture: " + error.responseText);
            }
        });
    });

    $("#OdysseoPres").click(function() {
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify({ action: "start_behavior", behavior: "welcome-odysseo/behavior_1" }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log("Comportement lancé: " + response.message);
            },
            error: function(error) {
                alert("Erreur lors du lancement du comportement: " + error.responseText);
            }
        });
    });

    $("#de").click(function() {
        $.ajax({
                url: "/",
                type: "POST",
                data: JSON.stringify({ action: "start_behavior", behavior: "sharkpresentation-b89c11/RaiseArm" }),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(response) {
                    console.log("Comportement lancé: " + response.message);
                },
                error: function(error) {
                    alert("Erreur lors du lancement du comportement: " + error.responseText);
                }
        });
    });

    $("#me, #me_2, #fear, #fear_2, #notConvived, #notConvived_2, #sharksFish, #sharksFish_2, #ears, #lookAtAquarium, #Exclamation, #Exclamation_2, #weAreSharks, #No, #No_2, #Excited, #Excited_2, #interessted, #interessted_2, #askVisitors, #askVisitors_2, #bodyBuilding, #bodyBuilding_2, #iKnow, #iKnow_2, #protectSharks, #protectSharks_2, #likeSharks, #likeSharks_2, #dancePropose, #dancePropose_2, #start_baby_shark_dance, #thanks, #thanks_2").click(function(event) {
        var behavior;

        console.log(this.id);

        if (this.id === "me") {
            behavior = "sharkpresentation-b89c11/RaiseArm";
        } else if (this.id === "me_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "fear") {
            behavior = "sharkpresentation-b89c11/FearSharks";
        } else if (this.id === "fear_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "notConvived") {
            behavior = "sharkpresentation-b89c11/Thinking";
        } else if (this.id === "notConvived_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "sharksFish") {
            behavior = "sharkpresentation-b89c11/InteruptOpenArms";
        } else if (this.id === "sharksFish_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "ears") {
            behavior = "sharkpresentation-b89c11/TouchingEars";
        } else if (this.id === "lookAtAquarium") {
            behavior = "sharkpresentation-b89c11/turnBothSides";
        } else if (this.id === "Exclamation") {
            behavior = "sharkpresentation-b89c11/Exclamation";
        } else if (this.id === "Exclamation_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "weAreSharks") {
            behavior = "sharkpresentation-b89c11/WeAreSharks";
        } else if (this.id === "No") {
            behavior = "sharkpresentation-b89c11/No";
        } else if (this.id === "No_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "Excited") {
            behavior = "sharkpresentation-b89c11/Excited";
        } else if (this.id === "Excited_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "interessted") {
            behavior = "sharkpresentation-b89c11/Interst_about_sharks";
        } else if (this.id === "interessted_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "askVisitors") {
            behavior = "sharkpresentation-b89c11/AskToVisitors";
        } else if (this.id === "askVisitors_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "bodyBuilding") {
            behavior = "sharkpresentation-b89c11/BodyBuilding_Pose";
        } else if (this.id === "bodyBuilding_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "iKnow") {
            behavior = "sharkpresentation-b89c11/Nao_Knows";
        } else if (this.id === "iKnow_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "protectSharks") {
            behavior = "sharkpresentation-b89c11/Why_protect_sharks";
        } else if (this.id === "protectSharks_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "likeSharks") {
            behavior = "sharkpresentation-b89c11/Feels_good_about_sharks";
        } else if (this.id === "likeSharks_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "dancePropose") {
            behavior = "sharkpresentation-b89c11/bby_shark_propose";
        } else if (this.id === "dancePropose_2") {
            behavior = "other_behavior_name";
        } else if (this.id === "start_baby_shark_dance") {
            behavior = "sharkpresentation-b89c11/bby_shark_dance";
        } else if (this.id === "thanks") {
            behavior = "sharkpresentation-b89c11/Thanks";
        } else if (this.id === "thanks_2") {
            behavior = "other_behavior_name";
        } else {
            behavior = "";
        }

        if (behavior !== "") {
            $.ajax({
                url: "/",
                type: "POST",
                data: JSON.stringify({ action: "start_behavior", behavior: behavior }),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(response) {
                    console.log("Comportement lancé: " + response.message);
                },
                error: function(error) {
                    alert("Erreur lors du lancement du comportement: " + error.responseText);
                }
            });
        }

    });

});