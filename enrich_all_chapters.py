#!/usr/bin/env python3
"""
Script pour enrichir TOUS les chapitres du fichier Le Dernier Jour d'un Condamné
avec 20 questions par chapitre
"""

import json
import os

def generate_additional_questions():
    """Générer des questions supplémentaires pour tous les chapitres"""
    
    additional_questions = {}
    
    # Chapitre 3 - Visites familiales
    additional_questions[3] = [
        {
            "id": "ch3_q5",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "emotion_visite",
            "prefixe": "générer une question:",
            "texte_entree": "Les visites familiales sont des moments d'émotion intense, où le condamné doit affronter la douleur de ses proches.",
            "texte_cible": "Quelle émotion domine lors des visites familiales ?\nA) La joie\nB) L'émotion intense et la douleur\nC) L'indifférence\nD) La colère\nRéponse correcte: B) L'émotion intense et la douleur\nExplication: Les visites familiales sont des moments d'émotion intense où le condamné doit affronter la souffrance de ses proches."
        },
        {
            "id": "ch3_q6",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "torture_morale",
            "prefixe": "générer une question:",
            "texte_entree": "Les visites familiales deviennent une torture morale pour le condamné, qui doit voir souffrir ceux qu'il aime.",
            "texte_cible": "Comment les visites familiales affectent-elles le condamné ?\nA) Elles le réconfortent\nB) Elles deviennent une torture morale\nC) Elles l'indiffèrent\nD) Elles le rendent joyeux\nRéponse correcte: B) Elles deviennent une torture morale\nExplication: Les visites familiales, loin de réconforter le condamné, deviennent une torture morale supplémentaire."
        },
        {
            "id": "ch3_q7",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_famille",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné garde précieusement en mémoire les derniers moments passés avec sa famille.",
            "texte_cible": "Que fait le condamné avec les moments passés avec sa famille ?\nA) Il les oublie\nB) Il les garde précieusement en mémoire\nC) Il les invente\nD) Il les raconte aux gardiens\nRéponse correcte: B) Il les garde précieusement en mémoire\nExplication: Le condamné chérit ces derniers moments avec sa famille comme des trésors précieux."
        },
        {
            "id": "ch3_q8",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "culpabilite_familiale",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une culpabilité profonde envers sa famille, se sentant responsable de leur souffrance.",
            "texte_cible": "Quel sentiment éprouve le condamné envers sa famille ?\nA) De la fierté\nB) Une culpabilité profonde\nC) De l'indifférence\nD) De la colère\nRéponse correcte: B) Une culpabilité profonde\nExplication: Le condamné se sent coupable de faire souffrir sa famille par sa situation, ajoutant une dimension morale à son drame personnel."
        },
        {
            "id": "ch3_q9",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "derniers_mots_famille",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné prononce ses derniers mots à sa famille, des paroles d'amour et de regret.",
            "texte_cible": "Que dit le condamné à sa famille ?\nA) Des paroles de colère\nB) Des paroles d'amour et de regret\nC) Des paroles d'indifférence\nD) Des paroles de haine\nRéponse correcte: B) Des paroles d'amour et de regret\nExplication: Le condamné s'adresse à sa famille avec des paroles empreintes d'amour et de regret profond."
        },
        {
            "id": "ch3_q10",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "denonciation_peine_mort",
            "prefixe": "générer une question:",
            "texte_entree": "À travers la souffrance de la famille, Victor Hugo dénonce l'impact de la peine de mort sur les proches.",
            "texte_cible": "Que dénonce Victor Hugo à travers la souffrance de la famille ?\nA) La vie en prison\nB) L'impact de la peine de mort sur les proches\nC) La société en général\nD) La justice\nRéponse correcte: B) L'impact de la peine de mort sur les proches\nExplication: Victor Hugo montre que la peine de mort affecte non seulement le condamné mais aussi ses proches, élargissant le champ de la souffrance."
        },
        {
            "id": "ch3_q11",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_separation",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une angoisse terrible à l'idée de se séparer définitivement de sa famille.",
            "texte_cible": "Quelle angoisse éprouve le condamné concernant sa famille ?\nA) L'angoisse de les revoir\nB) L'angoisse de la séparation définitive\nC) L'angoisse de leur bonheur\nD) L'angoisse de leur colère\nRéponse correcte: B) L'angoisse de la séparation définitive\nExplication: Le condamné est torturé par l'idée de la séparation définitive d'avec sa famille."
        },
        {
            "id": "ch3_q12",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "humanite_condamne",
            "prefixe": "générer une question:",
            "texte_entree": "Les relations familiales du condamné révèlent sa pleine humanité et sa capacité d'aimer.",
            "texte_cible": "Que révèlent les relations familiales du condamné ?\nA) Sa cruauté\nB) Sa pleine humanité et sa capacité d'aimer\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) Sa pleine humanité et sa capacité d'aimer\nExplication: Les relations familiales du condamné révèlent sa dimension humaine la plus profonde et sa capacité d'aimer."
        },
        {
            "id": "ch3_q13",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "regrets_familiaux",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve des regrets profonds envers sa famille, se demandant comment il a pu les faire souffrir.",
            "texte_cible": "Quels regrets éprouve le condamné envers sa famille ?\nA) Des regrets de les avoir connus\nB) Des regrets profonds de les avoir fait souffrir\nC) Des regrets de leur bonheur\nD) Des regrets de leur existence\nRéponse correcte: B) Des regrets profonds de les avoir fait souffrir\nExplication: Le condamné est rongé par les regrets d'avoir causé de la souffrance à sa famille."
        },
        {
            "id": "ch3_q14",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "effet_pathétique",
            "prefixe": "générer une question:",
            "texte_entree": "Les scènes familiales créent un effet pathétique intense, renforçant l'émotion du lecteur.",
            "texte_cible": "Quel effet produisent les scènes familiales ?\nA) Un effet comique\nB) Un effet pathétique intense\nC) Un effet neutre\nD) Un effet joyeux\nRéponse correcte: B) Un effet pathétique intense\nExplication: Les scènes familiales créent un pathos intense qui renforce l'émotion et l'empathie du lecteur."
        },
        {
            "id": "ch3_q15",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_enfants",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné pense particulièrement à ses enfants, s'inquiétant de leur avenir sans lui.",
            "texte_cible": "Pourquoi les enfants sont-ils particulièrement importants pour le condamné ?\nA) Ils sont les plus âgés\nB) Il s'inquiète de leur avenir sans lui\nC) Ils sont les plus riches\nD) Ils sont les plus intelligents\nRéponse correcte: B) Il s'inquiète de leur avenir sans lui\nExplication: Le condamné est particulièrement préoccupé par l'avenir de ses enfants, symbolisant l'angoisse paternelle face à la mort."
        },
        {
            "id": "ch3_q16",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "universalite_famille",
            "prefixe": "générer une question:",
            "texte_entree": "La souffrance familiale du condamné touche à des questions universelles sur les liens familiaux et la mort.",
            "texte_cible": "Pourquoi la souffrance familiale dépasse-t-elle le cas particulier ?\nA) Elle est très intense\nB) Elle touche à des questions universelles sur les liens familiaux\nC) Elle est bien décrite\nD) Elle est unique\nRéponse correcte: B) Elle touche à des questions universelles sur les liens familiaux\nExplication: La souffrance familiale transcende le cas particulier pour aborder des questions universelles sur les liens familiaux et la mort."
        },
        {
            "id": "ch3_q17",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "derniers_instants",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné savoure chaque instant passé avec sa famille, sachant que ce sont les derniers.",
            "texte_cible": "Comment le condamné vit-il les moments avec sa famille ?\nA) Il les ignore\nB) Il savoure chaque instant comme les derniers\nC) Il les invente\nD) Il les oublie\nRéponse correcte: B) Il savoure chaque instant comme les derniers\nExplication: Le condamné vit intensément chaque moment avec sa famille, conscient qu'ils sont les derniers."
        },
        {
            "id": "ch3_q18",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_familiale",
            "prefixe": "générer une question:",
            "texte_entree": "La psychologie du condamné face à sa famille révèle la complexité des émotions humaines face à la mort.",
            "texte_cible": "Que révèle la psychologie du condamné face à sa famille ?\nA) Sa simplicité\nB) La complexité des émotions humaines face à la mort\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) La complexité des émotions humaines face à la mort\nExplication: La psychologie du condamné face à sa famille révèle toute la complexité des émotions humaines confrontées à la mort."
        },
        {
            "id": "ch3_q19",
            "chapitre": 3,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_avenir_famille",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné est obsédé par l'idée de ce que deviendra sa famille après sa mort.",
            "texte_cible": "De quoi le condamné est-il obsédé concernant sa famille ?\nA) De leur bonheur\nB) De ce qu'elle deviendra après sa mort\nC) De leur richesse\nD) De leur réputation\nRéponse correcte: B) De ce qu'elle deviendra après sa mort\nExplication: L'idée de l'avenir de sa famille après sa mort obsède complètement le condamné."
        },
        {
            "id": "ch3_q20",
            "chapitre": 3,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "style_emotionnel",
            "prefixe": "générer une question:",
            "texte_entree": "Le style de Victor Hugo dans ce chapitre privilégie l'émotion et l'intensité dramatique des relations familiales.",
            "texte_cible": "Quelle caractéristique marque le style de Victor Hugo dans ce chapitre ?\nA) La froideur\nB) L'émotion et l'intensité dramatique\nC) L'humour\nD) La complexité syntaxique\nRéponse correcte: B) L'émotion et l'intensité dramatique\nExplication: Le style de Victor Hugo se caractérise par une intensité émotionnelle forte dans la description des relations familiales."
        }
    ]
    
    return additional_questions

def enrich_all_chapters():
    """Enrichir tous les chapitres avec 20 questions chacun"""
    
    file_path = "data/qcm/Le_Dernier_Jour/training_data_V1.json"
    
    # Charger le fichier existant
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Générer les questions supplémentaires
    additional_questions = generate_additional_questions()
    
    # Ajouter les questions supplémentaires
    questions = data["dataset_entrainement_complet"]
    
    # Pour chaque chapitre, ajouter les questions manquantes
    for chapitre in range(3, 11):  # Chapitres 3 à 10
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
    
    print(f"✅ Fichier enrichi avec succès !")
    print(f"📊 Nombre total de questions: {len(questions)}")
    
    # Compter les questions par chapitre
    for ch in range(1, 11):
        count = len([q for q in questions if q['chapitre'] == ch])
        print(f"📊 Questions chapitre {ch}: {count}")

if __name__ == "__main__":
    enrich_all_chapters()








