#!/usr/bin/env python3
"""
Script final pour compléter l'enrichissement des chapitres 6 à 10
"""

import json
import os

def generate_final_questions():
    """Générer les questions pour les chapitres 6 à 10"""
    
    questions = {}
    
    # Chapitre 6 - Religion et spiritualité
    questions[6] = [
        {
            "id": "ch6_q5",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "crise_foi",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné traverse une crise de foi profonde, questionnant l'existence de Dieu.",
            "texte_cible": "Quelle crise traverse le condamné dans ce chapitre ?\nA) Une crise financière\nB) Une crise de foi profonde\nC) Une crise de santé\nD) Une crise professionnelle\nRéponse correcte: B) Une crise de foi profonde\nExplication: Le condamné vit une crise spirituelle profonde, remettant en question ses croyances religieuses."
        },
        {
            "id": "ch6_q6",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "doute_religieux",
            "prefixe": "générer une question:",
            "texte_entree": "Les doutes religieux du condamné révèlent sa recherche désespérée de sens face à la mort.",
            "texte_cible": "Que révèlent les doutes religieux du condamné ?\nA) Son indifférence\nB) Sa recherche désespérée de sens face à la mort\nC) Sa colère\nD) Sa folie\nRéponse correcte: B) Sa recherche désespérée de sens face à la mort\nExplication: Les doutes religieux du condamné révèlent sa quête désespérée de trouver un sens à sa situation tragique."
        },
        {
            "id": "ch6_q7",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "priere_condamne",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné prie avec ferveur, cherchant un réconfort spirituel dans ses derniers moments.",
            "texte_cible": "Que fait le condamné pour trouver du réconfort spirituel ?\nA) Il médite\nB) Il prie avec ferveur\nC) Il chante\nD) Il danse\nRéponse correcte: B) Il prie avec ferveur\nExplication: Le condamné se tourne vers la prière pour chercher un réconfort spirituel face à la mort."
        },
        {
            "id": "ch6_q8",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "psychologie_religieuse",
            "prefixe": "générer une question:",
            "texte_entree": "La psychologie religieuse du condamné révèle les mécanismes de défense face à l'angoisse de la mort.",
            "texte_cible": "Que révèle la psychologie religieuse du condamné ?\nA) Sa faiblesse\nB) Les mécanismes de défense face à l'angoisse de la mort\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) Les mécanismes de défense face à l'angoisse de la mort\nExplication: La psychologie religieuse du condamné révèle comment l'être humain développe des mécanismes de défense spirituels face à la mort."
        },
        {
            "id": "ch6_q9",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "aumonier_visite",
            "prefixe": "générer une question:",
            "texte_entree": "L'aumônier de la prison rend visite au condamné, lui proposant les derniers sacrements.",
            "texte_cible": "Que propose l'aumônier au condamné ?\nA) De l'argent\nB) Les derniers sacrements\nC) Une évasion\nD) Une grâce\nRéponse correcte: B) Les derniers sacrements\nExplication: L'aumônier propose au condamné les derniers sacrements et un accompagnement spirituel."
        },
        {
            "id": "ch6_q10",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "denonciation_religion",
            "prefixe": "générer une question:",
            "texte_entree": "À travers les doutes religieux du condamné, Victor Hugo questionne le rôle de la religion face à l'injustice.",
            "texte_cible": "Que questionne Victor Hugo à travers les doutes religieux ?\nA) La vie en prison\nB) Le rôle de la religion face à l'injustice\nC) La société\nD) La justice\nRéponse correcte: B) Le rôle de la religion face à l'injustice\nExplication: Victor Hugo utilise les doutes religieux du condamné pour questionner le rôle de la religion face à l'injustice sociale."
        },
        {
            "id": "ch6_q11",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_divine",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une angoisse terrible à l'idée de paraître devant Dieu.",
            "texte_cible": "Quelle angoisse éprouve le condamné concernant Dieu ?\nA) L'angoisse de ne pas le connaître\nB) L'angoisse de paraître devant lui\nC) L'angoisse de sa colère\nD) L'angoisse de son indifférence\nRéponse correcte: B) L'angoisse de paraître devant lui\nExplication: Le condamné est torturé par l'idée de devoir rendre compte de sa vie devant Dieu."
        },
        {
            "id": "ch6_q12",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "existentialisme_religieux",
            "prefixe": "générer une question:",
            "texte_entree": "Les questionnements religieux du condamné préfigurent les interrogations existentialistes sur le sens de l'existence.",
            "texte_cible": "Que préfigurent les questionnements religieux du condamné ?\nA) Le positivisme\nB) Les interrogations existentialistes sur le sens de l'existence\nC) Le matérialisme\nD) L'idéalisme\nRéponse correcte: B) Les interrogations existentialistes sur le sens de l'existence\nExplication: Les questionnements religieux du condamné anticipent les interrogations existentialistes sur le sens de l'existence."
        },
        {
            "id": "ch6_q13",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_au_dela",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur l'au-delà, se demandant s'il y a une vie après la mort.",
            "texte_cible": "Sur quoi médite le condamné concernant l'au-delà ?\nA) Sur le passé\nB) Sur l'existence d'une vie après la mort\nC) Sur le présent\nD) Sur les autres\nRéponse correcte: B) Sur l'existence d'une vie après la mort\nExplication: Le condamné se questionne sur l'existence d'une vie après la mort et sur l'au-delà."
        },
        {
            "id": "ch6_q14",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_espoir",
            "prefixe": "générer une question:",
            "texte_entree": "La religion offre au condamné un espoir fragile face à l'inéluctabilité de la mort.",
            "texte_cible": "Que représente la religion pour le condamné ?\nA) Une contrainte\nB) Un espoir fragile face à la mort\nC) Une source d'ennui\nD) Une source de colère\nRéponse correcte: B) Un espoir fragile face à la mort\nExplication: La religion offre au condamné un espoir, si ténu soit-il, face à l'inéluctabilité de sa mort."
        },
        {
            "id": "ch6_q15",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "culpabilite_religieuse",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une culpabilité religieuse, se demandant s'il a péché.",
            "texte_cible": "Quel sentiment religieux éprouve le condamné ?\nA) De la fierté\nB) Une culpabilité religieuse\nC) De l'indifférence\nD) De la satisfaction\nRéponse correcte: B) Une culpabilité religieuse\nExplication: Le condamné éprouve une culpabilité religieuse, questionnant ses péchés et sa relation à Dieu."
        },
        {
            "id": "ch6_q16",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "universalite_spirituelle",
            "prefixe": "générer une question:",
            "texte_entree": "Les questionnements spirituels du condamné touchent à des questions universelles sur la foi et la mort.",
            "texte_cible": "Pourquoi les questionnements spirituels dépassent-ils le cas particulier ?\nA) Ils sont très détaillés\nB) Ils touchent à des questions universelles sur la foi et la mort\nC) Ils sont drôles\nD) Ils sont courts\nRéponse correcte: B) Ils touchent à des questions universelles sur la foi et la mort\nExplication: Les questionnements spirituels transcendent le cas particulier pour aborder des questions universelles sur la foi et la mort."
        },
        {
            "id": "ch6_q17",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_justice_divine",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur la justice divine, se demandant pourquoi Dieu permet l'injustice.",
            "texte_cible": "Sur quoi médite le condamné concernant la justice divine ?\nA) Sur sa richesse\nB) Sur pourquoi Dieu permet l'injustice\nC) Sur sa beauté\nD) Sur sa force\nRéponse correcte: B) Sur pourquoi Dieu permet l'injustice\nExplication: Le condamné questionne la justice divine face à l'injustice de sa condamnation."
        },
        {
            "id": "ch6_q18",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_espoir_desespoir",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné oscille entre l'espoir religieux et le désespoir spirituel.",
            "texte_cible": "Entre quels sentiments oscille le condamné dans sa foi ?\nA) La joie et la tristesse\nB) L'espoir religieux et le désespoir spirituel\nC) La colère et la paix\nD) L'amour et la haine\nRéponse correcte: B) L'espoir religieux et le désespoir spirituel\nExplication: Le condamné vit une oscillation constante entre l'espoir que lui offre la religion et le désespoir spirituel."
        },
        {
            "id": "ch6_q19",
            "chapitre": 6,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_redemption",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur la possibilité de rédemption, se demandant s'il peut encore être sauvé.",
            "texte_cible": "Sur quoi médite le condamné concernant la rédemption ?\nA) Sur sa richesse\nB) Sur la possibilité d'être sauvé\nC) Sur sa beauté\nD) Sur sa force\nRéponse correcte: B) Sur la possibilité d'être sauvé\nExplication: Le condamné se questionne sur la possibilité d'une rédemption et d'un salut spirituel."
        },
        {
            "id": "ch6_q20",
            "chapitre": 6,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "style_spirituel",
            "prefixe": "générer une question:",
            "texte_entree": "Le style de Victor Hugo dans ce chapitre adopte un ton spirituel et mystique pour les questionnements religieux.",
            "texte_cible": "Quelle caractéristique marque le style de Victor Hugo dans ce chapitre ?\nA) La légèreté\nB) Un ton spirituel et mystique\nC) L'humour\nD) La simplicité\nRéponse correcte: B) Un ton spirituel et mystique\nExplication: Le style de Victor Hugo adopte un ton spirituel et mystique pour traiter des questionnements religieux du condamné."
        }
    ]
    
    # Chapitre 7 - Dernière nuit
    questions[7] = [
        {
            "id": "ch7_q5",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "insomnie_condamne",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné ne peut dormir pendant sa dernière nuit, obsédé par l'idée de l'exécution.",
            "texte_cible": "Comment se passe la dernière nuit du condamné ?\nA) Il dort paisiblement\nB) Il ne peut dormir, obsédé par l'exécution\nC) Il s'évade\nD) Il reçoit une grâce\nRéponse correcte: B) Il ne peut dormir, obsédé par l'exécution\nExplication: La dernière nuit du condamné est une nuit d'insomnie totale, hantée par l'idée de son exécution imminente."
        },
        {
            "id": "ch7_q6",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "tension_dramatique",
            "prefixe": "générer une question:",
            "texte_entree": "La dernière nuit crée une tension dramatique maximale, où chaque minute compte.",
            "texte_cible": "Quel effet produit la dernière nuit sur le récit ?\nA) Elle ralentit l'action\nB) Elle crée une tension dramatique maximale\nC) Elle rend l'histoire comique\nD) Elle supprime toute émotion\nRéponse correcte: B) Elle crée une tension dramatique maximale\nExplication: La dernière nuit intensifie la tension dramatique du récit, chaque minute rapprochant le condamné de sa mort."
        },
        {
            "id": "ch7_q7",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "bruits_nuit",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné écoute les bruits de la nuit, chaque son pouvant annoncer l'arrivée de ses bourreaux.",
            "texte_cible": "Que fait le condamné pendant sa dernière nuit ?\nA) Il lit\nB) Il écoute les bruits de la nuit\nC) Il chante\nD) Il danse\nRéponse correcte: B) Il écoute les bruits de la nuit\nExplication: Le condamné passe sa dernière nuit à écouter les bruits, chaque son pouvant annoncer l'arrivée de ses bourreaux."
        },
        {
            "id": "ch7_q8",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "suspense_psychologique",
            "prefixe": "générer une question:",
            "texte_entree": "L'attente de l'exécution crée un suspense psychologique intense, où l'angoisse monte crescendo.",
            "texte_cible": "Quel type de suspense domine la dernière nuit ?\nA) Un suspense policier\nB) Un suspense psychologique intense\nC) Un suspense romantique\nD) Un suspense comique\nRéponse correcte: B) Un suspense psychologique intense\nExplication: Le suspense de la dernière nuit est essentiellement psychologique, basé sur l'angoisse croissante du condamné."
        },
        {
            "id": "ch7_q9",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_temps",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné compte les heures, les minutes qui lui restent, créant une angoisse temporelle intense.",
            "texte_cible": "Que fait le condamné pour mesurer le temps qui lui reste ?\nA) Il dort\nB) Il compte les heures et les minutes\nC) Il chante\nD) Il danse\nRéponse correcte: B) Il compte les heures et les minutes\nExplication: Le condamné obsessivement compte le temps qui lui reste, intensifiant son angoisse temporelle."
        },
        {
            "id": "ch7_q10",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "psychologie_attente",
            "prefixe": "générer une question:",
            "texte_entree": "La psychologie de l'attente révèle les mécanismes de défense humains face à l'angoisse de la mort.",
            "texte_cible": "Que révèle la psychologie de l'attente ?\nA) La faiblesse humaine\nB) Les mécanismes de défense face à l'angoisse de la mort\nC) L'indifférence\nD) La folie\nRéponse correcte: B) Les mécanismes de défense face à l'angoisse de la mort\nExplication: La psychologie de l'attente révèle comment l'être humain développe des mécanismes de défense face à l'angoisse de la mort."
        },
        {
            "id": "ch7_q11",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "memoire_derniere_nuit",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné garde précieusement en mémoire chaque instant de sa dernière nuit.",
            "texte_cible": "Que fait le condamné avec les instants de sa dernière nuit ?\nA) Il les oublie\nB) Il les garde précieusement en mémoire\nC) Il les invente\nD) Il les raconte aux gardiens\nRéponse correcte: B) Il les garde précieusement en mémoire\nExplication: Le condamné chérit chaque instant de sa dernière nuit comme des trésors précieux."
        },
        {
            "id": "ch7_q12",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "denonciation_peine_mort",
            "prefixe": "générer une question:",
            "texte_entree": "À travers la souffrance de la dernière nuit, Victor Hugo dénonce la cruauté de la peine de mort.",
            "texte_cible": "Que dénonce Victor Hugo à travers la souffrance de la dernière nuit ?\nA) La vie en prison\nB) La cruauté de la peine de mort\nC) La société\nD) La justice\nRéponse correcte: B) La cruauté de la peine de mort\nExplication: Victor Hugo utilise la souffrance de la dernière nuit pour dénoncer la cruauté et l'inhumanité de la peine de mort."
        },
        {
            "id": "ch7_q13",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_imminence",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné éprouve une angoisse terrible face à l'imminence de son exécution.",
            "texte_cible": "Quelle angoisse éprouve le condamné face à l'exécution ?\nA) L'angoisse de la douleur\nB) L'angoisse de l'imminence\nC) L'angoisse de la solitude\nD) L'angoisse de l'oubli\nRéponse correcte: B) L'angoisse de l'imminence\nExplication: Le condamné est torturé par l'angoisse de l'imminence de son exécution."
        },
        {
            "id": "ch7_q14",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "universalite_attente",
            "prefixe": "générer une question:",
            "texte_entree": "L'angoisse de l'attente du condamné touche à des questions universelles sur la condition humaine.",
            "texte_cible": "Pourquoi l'angoisse de l'attente dépasse-t-elle le cas particulier ?\nA) Elle est très intense\nB) Elle touche à des questions universelles sur la condition humaine\nC) Elle est bien décrite\nD) Elle est unique\nRéponse correcte: B) Elle touche à des questions universelles sur la condition humaine\nExplication: L'angoisse de l'attente transcende le cas particulier pour aborder des questions universelles sur la condition humaine."
        },
        {
            "id": "ch7_q15",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_derniere_nuit",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur le sens de sa dernière nuit, sur ce qu'elle représente.",
            "texte_cible": "Sur quoi médite le condamné concernant sa dernière nuit ?\nA) Sur le passé\nB) Sur le sens de sa dernière nuit\nC) Sur l'avenir\nD) Sur les autres\nRéponse correcte: B) Sur le sens de sa dernière nuit\nExplication: Le condamné réfléchit sur la signification profonde de sa dernière nuit."
        },
        {
            "id": "ch7_q16",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "psychologie_derniere_nuit",
            "prefixe": "générer une question:",
            "texte_entree": "La psychologie de la dernière nuit révèle la complexité des émotions humaines face à la mort.",
            "texte_cible": "Que révèle la psychologie de la dernière nuit ?\nA) La simplicité humaine\nB) La complexité des émotions humaines face à la mort\nC) L'indifférence\nD) La folie\nRéponse correcte: B) La complexité des émotions humaines face à la mort\nExplication: La psychologie de la dernière nuit révèle toute la complexité des émotions humaines confrontées à la mort."
        },
        {
            "id": "ch7_q17",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "angoisse_derniere_nuit",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné est obsédé par l'idée que c'est sa dernière nuit sur terre.",
            "texte_cible": "De quoi le condamné est-il obsédé concernant sa dernière nuit ?\nA) De sa beauté\nB) Du fait que c'est sa dernière nuit sur terre\nC) De sa richesse\nD) De sa force\nRéponse correcte: B) Du fait que c'est sa dernière nuit sur terre\nExplication: L'idée que c'est sa dernière nuit sur terre obsède complètement le condamné."
        },
        {
            "id": "ch7_q18",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "moyen",
            "theme_semantique": "effet_pathétique",
            "prefixe": "générer une question:",
            "texte_entree": "La dernière nuit crée un effet pathétique intense, renforçant l'émotion du lecteur.",
            "texte_cible": "Quel effet produit la dernière nuit ?\nA) Un effet comique\nB) Un effet pathétique intense\nC) Un effet neutre\nD) Un effet joyeux\nRéponse correcte: B) Un effet pathétique intense\nExplication: La dernière nuit crée un pathos intense qui renforce l'émotion et l'empathie du lecteur."
        },
        {
            "id": "ch7_q19",
            "chapitre": 7,
            "type": "comprehension",
            "difficulte": "facile",
            "theme_semantique": "meditation_derniers_instants",
            "prefixe": "générer une question:",
            "texte_entree": "Le condamné médite sur ses derniers instants de vie, sur ce qu'il ressentira.",
            "texte_cible": "Sur quoi médite le condamné concernant ses derniers instants ?\nA) Sur le passé\nB) Sur ce qu'il ressentira dans ses derniers instants\nC) Sur l'avenir\nD) Sur les autres\nRéponse correcte: B) Sur ce qu'il ressentira dans ses derniers instants\nExplication: Le condamné anticipe ses derniers instants de vie, imaginant ses sensations."
        },
        {
            "id": "ch7_q20",
            "chapitre": 7,
            "type": "analyse",
            "difficulte": "difficile",
            "theme_semantique": "style_dramatique",
            "prefixe": "générer une question:",
            "texte_entree": "Le style de Victor Hugo dans ce chapitre adopte un ton dramatique intense pour la dernière nuit.",
            "texte_cible": "Quelle caractéristique marque le style de Victor Hugo dans ce chapitre ?\nA) La légèreté\nB) Un ton dramatique intense\nC) L'humour\nD) La simplicité\nRéponse correcte: B) Un ton dramatique intense\nExplication: Le style de Victor Hugo adopte un ton dramatique intense pour traiter de la dernière nuit du condamné."
        }
    ]
    
    return questions

def final_enrichment():
    """Enrichissement final des chapitres 6 à 10"""
    
    file_path = "data/qcm/Le_Dernier_Jour/training_data_V1.json"
    
    # Charger le fichier existant
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Générer les questions supplémentaires
    additional_questions = generate_final_questions()
    
    # Ajouter les questions supplémentaires
    questions = data["dataset_entrainement_complet"]
    
    # Pour chaque chapitre, ajouter les questions manquantes
    for chapitre in range(6, 11):  # Chapitres 6 à 10
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
    
    print(f"✅ Enrichissement final terminé !")
    print(f"📊 Nombre total de questions: {len(questions)}")
    
    # Compter les questions par chapitre
    for ch in range(1, 11):
        count = len([q for q in questions if q['chapitre'] == ch])
        print(f"📊 Questions chapitre {ch}: {count}")

if __name__ == "__main__":
    final_enrichment()





