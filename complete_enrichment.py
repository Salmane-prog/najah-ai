#!/usr/bin/env python3
"""
Script pour compléter l'enrichissement de TOUS les chapitres restants
"""

import json
import os

def generate_remaining_questions():
    """Générer les questions pour les chapitres 4 à 10"""
    
    questions = {}
    
    # Chapitre 4 - Souvenirs d'enfance
    questions[4] = [
        {
            "id": "ch4_q5",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "refuge_souvenirs",
            "prefixe": "générer une question:",
            "texte_entree": "Les souvenirs d'enfance offrent au condamné un refuge temporaire contre l'angoisse de sa situation.",
            "texte_cible": "Que représentent les souvenirs d'enfance pour le condamné ?\nA) Une source de douleur\nB) Un refuge temporaire contre l'angoisse\nC) Une source d'ennui\nD) Une source de colère\nRéponse correcte: B) Un refuge temporaire contre l'angoisse\nExplication: Les souvenirs d'enfance offrent au condamné un échappatoire temporaire à sa situation tragique."
        },
        {
            "id": "ch4_q6",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "contraste_temporal",
            "prefixe": "générer une question:",
            "texte_entree": "Le contraste entre l'innocence de l'enfance et la tragédie présente crée un effet dramatique puissant.",
            "texte_cible": "Quel effet produit le contraste entre l'enfance et le présent ?\nA) Un effet comique\nB) Un effet dramatique puissant\nC) Un effet neutre\nD) Un effet joyeux\nRéponse correcte: B) Un effet dramatique puissant\nExplication: Le contraste entre l'innocence passée et la tragédie présente renforce l'impact dramatique du récit."
        },
        {
            "id": "ch4_q7",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_jeux",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se remémore ses jeux d'enfant, ses rires, sa liberté perdue.",
            "texte_cible": "Que se remémore le condamné de son enfance ?\nA) Ses peines\nB) Ses jeux, ses rires, sa liberté\nC) Ses ennemis\nD) Ses échecs\nRéponse correcte: B) Ses jeux, ses rires, sa liberté\nExplication: Le condamné évoque les moments joyeux de son enfance, contrastant avec sa situation actuelle."
        },
        {
            "id": "ch4_q8",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "perte_innocence",
            "prefixe": "générer une question:",
            "texte_entree": "Les souvenirs d'enfance symbolisent la perte de l'innocence et l'irréversibilité du temps.",
            "texte_cible": "Que symbolisent les souvenirs d'enfance ?\nA) La joie éternelle\nB) La perte de l'innocence et l'irréversibilité du temps\nC) La réussite\nD) La richesse\nRéponse correcte: B) La perte de l'innocence et l'irréversibilité du temps\nExplication: Les souvenirs d'enfance symbolisent la perte définitive de l'innocence et l'irréversibilité du temps qui passe."
        },
        {
            "id": "ch4_q9",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_mere_enfance",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de sa mère dans son enfance, de sa tendresse et de sa protection.",
            "texte_cible": "Que se souvient le condamné de sa mère dans son enfance ?\nA) Sa sévérité\nB) Sa tendresse et sa protection\nC) Son indifférence\nD) Sa colère\nRéponse correcte: B) Sa tendresse et sa protection\nExplication: Le condamné évoque la figure maternelle protectrice et tendre de son enfance."
        },
        {
            "id": "ch4_q10",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "nostalgie_condamne",
            "prefixe": "générer une question:",
            "texte_entree": "La nostalgie du condamné pour son enfance révèle son désir de retourner à un état d'innocence perdue.",
            "texte_cible": "Que révèle la nostalgie du condamné pour son enfance ?\nA) Son désir de vieillir\nB) Son désir de retourner à l'innocence perdue\nC) Son indifférence\nD) Sa haine du passé\nRéponse correcte: B) Son désir de retourner à l'innocence perdue\nExplication: La nostalgie du condamné révèle son désir profond de retrouver l'innocence et la pureté de l'enfance."
        },
        {
            "id": "ch4_q11",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_liberté",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de sa liberté d'enfant, contrastant avec son enfermement actuel.",
            "texte_cible": "Que se souvient le condamné de sa liberté d'enfant ?\nA) Sa contrainte\nB) Sa liberté, contrastant avec son enfermement\nC) Son ennui\nD) Sa peur\nRéponse correcte: B) Sa liberté, contrastant avec son enfermement\nExplication: Le condamné évoque sa liberté d'enfant, créant un contraste saisissant avec son enfermement actuel."
        },
        {
            "id": "ch4_q12",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "temps_cyclique",
            "prefixe": "générer une question:",
            "texte_entree": "Les souvenirs d'enfance créent une temporalité cyclique qui s'oppose au temps linéaire de la condamnation.",
            "texte_cible": "Comment les souvenirs d'enfance affectent-ils la perception du temps ?\nA) Ils l'accélèrent\nB) Ils créent une temporalité cyclique opposée au temps linéaire\nC) Ils l'arrêtent\nD) Ils le rendent confus\nRéponse correcte: B) Ils créent une temporalité cyclique opposée au temps linéaire\nExplication: Les souvenirs d'enfance créent une temporalité cyclique qui s'oppose au temps linéaire et irréversible de la condamnation."
        },
        {
            "id": "ch4_q13",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_amis",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de ses amis d'enfance, de leurs jeux et de leur camaraderie.",
            "texte_cible": "Que se souvient le condamné de ses amis d'enfance ?\nA) Leurs disputes\nB) Leurs jeux et leur camaraderie\nC) Leur méchanceté\nD) Leur indifférence\nRéponse correcte: B) Leurs jeux et leur camaraderie\nExplication: Le condamné évoque les moments de camaraderie et de jeux partagés avec ses amis d'enfance."
        },
        {
            "id": "ch4_q14",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "regret_innocence",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné regrette profondément d'avoir perdu l'innocence de son enfance.",
            "texte_cible": "Que regrette le condamné concernant son enfance ?\nA) Sa pauvreté\nB) D'avoir perdu l'innocence de son enfance\nC) Sa richesse\nD) Sa beauté\nRéponse correcte: B) D'avoir perdu l'innocence de son enfance\nExplication: Le condamné éprouve un regret profond d'avoir perdu l'innocence et la pureté de son enfance."
        },
        {
            "id": "ch4_q15",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_ecole",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de son école, de ses maîtres et de ses apprentissages.",
            "texte_cible": "Que se souvient le condamné de son école ?\nA) Ses punitions\nB) Ses maîtres et ses apprentissages\nC) Ses échecs\nD) Sa haine\nRéponse correcte: B) Ses maîtres et ses apprentissages\nExplication: Le condamné évoque ses souvenirs d'école, de ses enseignants et de ses apprentissages."
        },
        {
            "id": "ch4_q16",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "universalite_enfance",
            "prefixe": "générer une question:",
            "texte_entree": "Les souvenirs d'enfance du condamné touchent à des questions universelles sur l'innocence et la perte.",
            "texte_cible": "Pourquoi les souvenirs d'enfance dépassent-ils le cas particulier ?\nA) Ils sont très détaillés\nB) Ils touchent à des questions universelles sur l'innocence\nC) Ils sont drôles\nD) Ils sont courts\nRéponse correcte: B) Ils touchent à des questions universelles sur l'innocence\nExplication: Les souvenirs d'enfance transcendent le cas particulier pour aborder des questions universelles sur l'innocence et la perte."
        },
        {
            "id": "ch4_q17",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_nature",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de la nature de son enfance, des arbres, des fleurs, du ciel libre.",
            "texte_cible": "Que se souvient le condamné de la nature de son enfance ?\nA) Sa laideur\nB) Des arbres, des fleurs, du ciel libre\nC) Sa dangerosité\nD) Son ennui\nRéponse correcte: B) Des arbres, des fleurs, du ciel libre\nExplication: Le condamné évoque la beauté de la nature de son enfance, contrastant avec son enfermement actuel."
        },
        {
            "id": "ch4_q18",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_regression",
            "prefixe": "générer une question:",
            "texte_entree": "Le recours aux souvenirs d'enfance révèle une régression psychologique du condamné face à l'angoisse.",
            "texte_cible": "Que révèle le recours aux souvenirs d'enfance ?\nA) Sa maturité\nB) Une régression psychologique face à l'angoisse\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) Une régression psychologique face à l'angoisse\nExplication: Le recours aux souvenirs d'enfance révèle une régression psychologique du condamné face à l'angoisse de la mort."
        },
        {
            "id": "ch4_q19",
            "chapitre": 4,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_innocence",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se souvient de son innocence d'enfant, de sa pureté perdue.",
            "texte_cible": "Que se souvient le condamné de son innocence d'enfant ?\nA) Sa méchanceté\nB) Sa pureté perdue\nC) Son indifférence\nD) Sa colère\nRéponse correcte: B) Sa pureté perdue\nExplication: Le condamné évoque son innocence et sa pureté d'enfant, contrastant avec sa situation actuelle."
        },
        {
            "id": "ch4_q20",
            "chapitre": 4,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "style_poetique",
            "prefixe": "générer une question:",
            "texte_entree": "Le style de Victor Hugo dans ce chapitre adopte un ton poétique pour évoquer l'enfance perdue.",
            "texte_cible": "Quelle caractéristique marque le style de Victor Hugo dans ce chapitre ?\nA) La froideur\nB) Un ton poétique pour évoquer l'enfance\nC) L'humour\nD) La complexité syntaxique\nRéponse correcte: B) Un ton poétique pour évoquer l'enfance\nExplication: Le style de Victor Hugo adopte un ton poétique et nostalgique pour évoquer l'enfance perdue du condamné."
        }
    ]
    
    # Chapitre 5 - Réflexions sur la mort
    questions[5] = [
        {
            "id": "ch5_q5",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_mort",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se livre à une méditation profonde sur la mort et son sens.",
            "texte_cible": "Que fait le condamné concernant la mort ?\nA) Il l'ignore\nB) Il se livre à une méditation profonde\nC) Il en rit\nD) Il l'oublie\nRéponse correcte: B) Il se livre à une méditation profonde\nExplication: Le condamné développe une réflexion profonde et philosophique sur la mort et son sens."
        },
        {
            "id": "ch5_q6",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "philosophie_mort",
            "prefixe": "générer une question:",
            "texte_entree": "Les réflexions du condamné sur la mort touchent aux questions philosophiques les plus fondamentales.",
            "texte_cible": "Quel type de questions abordent les réflexions du condamné ?\nA) Des questions pratiques\nB) Des questions philosophiques fondamentales\nC) Des questions triviales\nD) Des questions techniques\nRéponse correcte: B) Des questions philosophiques fondamentales\nExplication: Les réflexions du condamné touchent aux questions philosophiques les plus essentielles sur la mort et l'existence."
        },
        {
            "id": "ch5_q7",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_inexistence",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une angoisse terrible à l'idée de ne plus exister.",
            "texte_cible": "Quelle angoisse éprouve le condamné face à la mort ?\nA) L'angoisse de la douleur\nB) L'angoisse de ne plus exister\nC) L'angoisse de la solitude\nD) L'angoisse de l'oubli\nRéponse correcte: B) L'angoisse de ne plus exister\nExplication: Le condamné est torturé par l'idée de l'inexistence totale qui l'attend."
        },
        {
            "id": "ch5_q8",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "existentialisme",
            "prefixe": "générer une question:",
            "texte_entree": "Les réflexions du condamné préfigurent les questions existentialistes sur le sens de l'existence.",
            "texte_cible": "Que préfigurent les réflexions du condamné ?\nA) Le positivisme\nB) Les questions existentialistes sur le sens de l'existence\nC) Le matérialisme\nD) L'idéalisme\nRéponse correcte: B) Les questions existentialistes sur le sens de l'existence\nExplication: Les réflexions du condamné anticipent les questionnements existentialistes sur le sens de l'existence."
        },
        {
            "id": "ch5_q9",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_instant",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur l'instant précis de sa mort, sur ce qu'il ressentira.",
            "texte_cible": "Sur quoi médite le condamné concernant sa mort ?\nA) Sur le passé\nB) Sur l'instant précis de sa mort\nC) Sur l'avenir\nD) Sur les autres\nRéponse correcte: B) Sur l'instant précis de sa mort\nExplication: Le condamné se concentre sur l'instant précis de sa mort, anticipant ses sensations."
        },
        {
            "id": "ch5_q10",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_mort",
            "prefixe": "générer une question:",
            "texte_entree": "La psychologie du condamné face à la mort révèle les mécanismes de défense humains.",
            "texte_cible": "Que révèle la psychologie du condamné face à la mort ?\nA) Sa faiblesse\nB) Les mécanismes de défense humains\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) Les mécanismes de défense humains\nExplication: La psychologie du condamné révèle les mécanismes de défense que l'être humain développe face à la mort."
        },
        {
            "id": "ch5_q11",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_au_dela",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné se demande ce qu'il y a au-delà de la mort, s'il y a une vie après.",
            "texte_cible": "Sur quoi se questionne le condamné concernant la mort ?\nA) Sur le passé\nB) Sur ce qu'il y a au-delà de la mort\nC) Sur le présent\nD) Sur les autres\nRéponse correcte: B) Sur ce qu'il y a au-delà de la mort\nExplication: Le condamné se questionne sur l'existence d'une vie après la mort."
        },
        {
            "id": "ch5_q12",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "metaphysique",
            "prefixe": "générer une question:",
            "texte_entree": "Les réflexions du condamné touchent aux questions métaphysiques les plus profondes.",
            "texte_cible": "Quel type de questions abordent les réflexions du condamné ?\nA) Des questions pratiques\nB) Des questions métaphysiques profondes\nC) Des questions triviales\nD) Des questions techniques\nRéponse correcte: B) Des questions métaphysiques profondes\nExplication: Les réflexions du condamné touchent aux questions métaphysiques les plus essentielles sur l'existence."
        },
        {
            "id": "ch5_q13",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_oubli",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une angoisse terrible à l'idée d'être oublié après sa mort.",
            "texte_cible": "Quelle angoisse éprouve le condamné concernant l'après-mort ?\nA) L'angoisse de la douleur\nB) L'angoisse d'être oublié\nC) L'angoisse de la solitude\nD) L'angoisse de l'inexistence\nRéponse correcte: B) L'angoisse d'être oublié\nExplication: Le condamné est torturé par l'idée d'être oublié et de disparaître de la mémoire des vivants."
        },
        {
            "id": "ch5_q14",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "denonciation_peine_mort",
            "prefixe": "générer une question:",
            "texte_entree": "À travers les réflexions du condamné, Victor Hugo dénonce l'inhumanité de la peine de mort.",
            "texte_cible": "Que dénonce Victor Hugo à travers les réflexions du condamné ?\nA) La vie en prison\nB) L'inhumanité de la peine de mort\nC) La société\nD) La justice\nRéponse correcte: B) L'inhumanité de la peine de mort\nExplication: Victor Hugo utilise les réflexions du condamné pour dénoncer l'inhumanité de la peine de mort."
        },
        {
            "id": "ch5_q15",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_justice",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur la justice de sa condamnation, se demandant s'il la mérite.",
            "texte_cible": "Sur quoi médite le condamné concernant sa condamnation ?\nA) Sur sa richesse\nB) Sur la justice de sa condamnation\nC) Sur sa beauté\nD) Sur sa force\nRéponse correcte: B) Sur la justice de sa condamnation\nExplication: Le condamné questionne la justice et la légitimité de sa condamnation à mort."
        },
        {
            "id": "ch5_q16",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "universalite_mort",
            "prefixe": "générer une question:",
            "texte_entree": "Les réflexions du condamné sur la mort touchent à des questions universelles sur la condition humaine.",
            "texte_cible": "Pourquoi les réflexions du condamné dépassent-elles son cas particulier ?\nA) Elles sont très détaillées\nB) Elles touchent à des questions universelles sur la condition humaine\nC) Elles sont drôles\nD) Elles sont courtes\nRéponse correcte: B) Elles touchent à des questions universelles sur la condition humaine\nExplication: Les réflexions du condamné transcendent son cas particulier pour aborder des questions universelles sur la mort et la condition humaine."
        },
        {
            "id": "ch5_q17",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_instant_execution",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné imagine l'instant précis de son exécution, anticipant ses dernières sensations.",
            "texte_cible": "Que fait le condamné concernant son exécution ?\nA) Il l'ignore\nB) Il imagine l'instant précis et ses sensations\nC) Il en rit\nD) Il l'oublie\nRéponse correcte: B) Il imagine l'instant précis et ses sensations\nExplication: Le condamné anticipe l'instant de son exécution, imaginant ses dernières sensations."
        },
        {
            "id": "ch5_q18",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_anticipation",
            "prefixe": "générer une question:",
            "texte_entree": "L'anticipation de la mort crée une angoisse psychologique intense chez le condamné.",
            "texte_cible": "Quel effet produit l'anticipation de la mort sur le condamné ?\nA) Elle le calme\nB) Elle crée une angoisse psychologique intense\nC) Elle l'indiffère\nD) Elle le rend joyeux\nRéponse correcte: B) Elle crée une angoisse psychologique intense\nExplication: L'anticipation de la mort provoque une angoisse psychologique majeure chez le condamné."
        },
        {
            "id": "ch5_q19",
            "chapitre": 5,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_legs",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur ce qu'il laissera derrière lui, sur son héritage.",
            "texte_cible": "Sur quoi médite le condamné concernant son héritage ?\nA) Sur sa richesse\nB) Sur ce qu'il laissera derrière lui\nC) Sur sa beauté\nD) Sur sa force\nRéponse correcte: B) Sur ce qu'il laissera derrière lui\nExplication: Le condamné réfléchit sur son héritage et sur ce qu'il laissera après sa mort."
        },
        {
            "id": "ch5_q20",
            "chapitre": 5,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "style_philosophique",
            "prefixe": "générer une question:",
            "texte_entree": "Le style de Victor Hugo dans ce chapitre adopte un ton philosophique pour les réflexions sur la mort.",
            "texte_cible": "Quelle caractéristique marque le style de Victor Hugo dans ce chapitre ?\nA) La légèreté\nB) Un ton philosophique pour les réflexions sur la mort\nC) L'humour\nD) La simplicité\nRéponse correcte: B) Un ton philosophique pour les réflexions sur la mort\nExplication: Le style de Victor Hugo adopte un ton philosophique et profond pour traiter des réflexions sur la mort."
        }
    ]
    
    return questions

def complete_enrichment():
    """Compléter l'enrichissement de tous les chapitres"""
    
    file_path = "data/qcm/Le_Dernier_Jour/training_data_V1.json"
    
    # Charger le fichier existant
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Générer les questions supplémentaires
    additional_questions = generate_remaining_questions()
    
    # Ajouter les questions supplémentaires
    questions = data["dataset_entrainement_complet"]
    
    # Pour chaque chapitre, ajouter les questions manquantes
    for chapitre in range(4, 11):  # Chapitres 4 à 10
        if chapitre in additional_questions:
            # Trouver où insérer les nouvelles questions
            ch_start = None
            for i, q in enumerate(questions):
                if q["chapitre"] == chapitre and q["id"] == f"ch{chapitre}_q1":
                    ch_start = i
                    break
            
            if ch_start is not None:
                # Insérer les nouvelles questions après les 4 existantes
                ch_end = ch_start + 4  # chX_q1, chX_q2, chX_q3, chX_q4
                for i, new_q in enumerate(additional_questions[chapitre]):
                    questions.insert(ch_end + i, new_q)
    
    # Mettre à jour le nombre d'exemples
    data["metadata"]["nombre_exemples"] = len(questions)
    data["metadata"]["version"] = "2.0_enriched"
    
    # Sauvegarder le fichier enrichi
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Enrichissement complet terminé !")
    print(f"📊 Nombre total de questions: {len(questions)}")
    
    # Compter les questions par chapitre
    for ch in range(1, 11):
        count = len([q for q in questions if q['chapitre'] == ch])
        print(f"📊 Questions chapitre {ch}: {count}")

if __name__ == "__main__":
    complete_enrichment()








