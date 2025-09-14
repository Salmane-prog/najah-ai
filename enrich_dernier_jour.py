#!/usr/bin/env python3
"""
Script pour enrichir le fichier Le Dernier Jour d'un Condamné
avec 20 questions par chapitre (actuellement 4 par chapitre)
"""

import json
import os

def enrich_questions():
    """Enrichir le fichier avec plus de questions"""
    
    file_path = "data/qcm/Le_Dernier_Jour/training_data_V1.json"
    
    # Charger le fichier existant
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Questions supplémentaires par chapitre
    additional_questions = {
        2: [
            {
                "id": "ch2_q5",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "memoire_enfance",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné se remémore des moments heureux de son enfance, contrastant avec sa situation actuelle tragique.",
                "texte_cible": "Que fait le condamné avec ses souvenirs d'enfance ?\nA) Il les oublie\nB) Il les évoque pour échapper à sa situation\nC) Il les invente\nD) Il les raconte aux gardiens\nRéponse correcte: B) Il les évoque pour échapper à sa situation\nExplication: Les souvenirs d'enfance offrent au condamné un refuge temporaire contre l'angoisse de sa situation présente."
            },
            {
                "id": "ch2_q6",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "moyen",
                "theme_semantique": "contraste_innocence_tragedie",
                "prefixe": "générer une question:",
                "texte_entree": "Les souvenirs d'enfance du condamné créent un contraste saisissant avec sa situation de condamné à mort.",
                "texte_cible": "Quel effet produit le contraste entre les souvenirs d'enfance et la situation présente ?\nA) Il rend le récit comique\nB) Il crée un effet pathétique saisissant\nC) Il rend l'histoire banale\nD) Il supprime toute émotion\nRéponse correcte: B) Il crée un effet pathétique saisissant\nExplication: Le contraste entre l'innocence des souvenirs d'enfance et la tragédie de la condamnation à mort renforce l'effet pathétique et émotionnel du récit."
            },
            {
                "id": "ch2_q7",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "reves_avenir",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné se souvient de ses rêves d'avenir, de ses projets, de tout ce qu'il n'aura jamais le temps de réaliser.",
                "texte_cible": "Que représentent les rêves d'avenir du condamné ?\nA) Des souvenirs heureux\nB) Tout ce qu'il n'aura jamais le temps de réaliser\nC) Des projets qu'il a accomplis\nD) Des regrets du passé\nRéponse correcte: B) Tout ce qu'il n'aura jamais le temps de réaliser\nExplication: Les rêves d'avenir du condamné symbolisent tout ce qui lui est désormais interdit, renforçant la tragédie de sa situation."
            },
            {
                "id": "ch2_q8",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "difficile",
                "theme_semantique": "temps_arrete",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné a l'impression que le temps s'est arrêté, que sa vie est figée dans l'attente de la mort.",
                "texte_cible": "Comment le condamné perçoit-il le temps qui passe ?\nA) Il passe très rapidement\nB) Il s'est arrêté, sa vie est figée\nC) Il est normal et régulier\nD) Il n'y pense pas\nRéponse correcte: B) Il s'est arrêté, sa vie est figée\nExplication: Le condamné vit dans une temporalité suspendue où le temps semble s'être arrêté, créant une atmosphère d'attente angoissante."
            },
            {
                "id": "ch2_q9",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "culpabilite_condamne",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné éprouve une culpabilité profonde, se demandant s'il mérite vraiment son sort et ce qu'il aurait pu faire pour l'éviter.",
                "texte_cible": "Quel sentiment éprouve le condamné envers sa situation ?\nA) De la fierté\nB) Une culpabilité profonde\nC) De l'indifférence\nD) De la satisfaction\nRéponse correcte: B) Une culpabilité profonde\nExplication: Le condamné est rongé par la culpabilité, questionnant la justice de sa condamnation et ses propres responsabilités."
            },
            {
                "id": "ch2_q10",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "moyen",
                "theme_semantique": "reflexion_justice",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné réfléchit sur la notion de justice, se demandant si sa condamnation est vraiment juste et équitable.",
                "texte_cible": "Sur quoi le condamné réfléchit-il concernant sa condamnation ?\nA) Sur ses projets d'avenir\nB) Sur la justice et l'équité de sa condamnation\nC) Sur ses souvenirs d'enfance\nD) Sur ses amis\nRéponse correcte: B) Sur la justice et l'équité de sa condamnation\nExplication: Le condamné développe une réflexion critique sur la justice, questionnant la légitimité de sa condamnation."
            },
            {
                "id": "ch2_q11",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "angoisse_famille",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné s'inquiète pour sa famille, se demandant comment elle va survivre sans lui et comment elle va supporter sa mort.",
                "texte_cible": "De quoi le condamné s'inquiète-t-il le plus pour sa famille ?\nA) De leur bonheur\nB) De leur survie et de leur souffrance\nC) De leur richesse\nD) De leur réputation\nRéponse correcte: B) De leur survie et de leur souffrance\nExplication: Le condamné est torturé par l'angoisse de la souffrance que sa mort va causer à sa famille."
            },
            {
                "id": "ch2_q12",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "difficile",
                "theme_semantique": "humanite_condamne",
                "prefixe": "générer une question:",
                "texte_entree": "À travers ses pensées et ses souvenirs, le condamné révèle sa pleine humanité, ses faiblesses et ses qualités.",
                "texte_cible": "Que révèlent les pensées du condamné sur sa nature ?\nA) Sa cruauté\nB) Sa pleine humanité avec ses faiblesses et qualités\nC) Son indifférence\nD) Sa folie\nRéponse correcte: B) Sa pleine humanité avec ses faiblesses et qualités\nExplication: Les pensées du condamné révèlent sa complexité humaine, mêlant faiblesses et qualités, le rendant profondément humain."
            },
            {
                "id": "ch2_q13",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "espoir_desespoir",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné oscille constamment entre l'espoir d'une grâce possible et le désespoir de sa situation inéluctable.",
                "texte_cible": "Entre quels sentiments le condamné oscille-t-il ?\nA) La joie et la tristesse\nB) L'espoir et le désespoir\nC) La colère et la paix\nD) L'amour et la haine\nRéponse correcte: B) L'espoir et le désespoir\nExplication: Le condamné vit une oscillation constante entre l'espoir d'une éventuelle grâce et le désespoir face à l'inéluctabilité de sa mort."
            },
            {
                "id": "ch2_q14",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "moyen",
                "theme_semantique": "denonciation_peine_mort",
                "prefixe": "générer une question:",
                "texte_entree": "En montrant la souffrance psychologique du condamné, Victor Hugo dénonce implicitement la cruauté de la peine de mort.",
                "texte_cible": "Que dénonce Victor Hugo à travers la souffrance du condamné ?\nA) La vie en prison\nB) La cruauté de la peine de mort\nC) La société en général\nD) La famille du condamné\nRéponse correcte: B) La cruauté de la peine de mort\nExplication: Victor Hugo utilise la souffrance psychologique du condamné pour dénoncer la cruauté et l'inhumanité de la peine de mort."
            },
            {
                "id": "ch2_q15",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "memoire_mere",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné se remémore particulièrement sa mère, évoquant des moments tendres et des regrets de ne plus la revoir.",
                "texte_cible": "Quel souvenir familial est particulièrement important pour le condamné ?\nA) Celui de son père\nB) Celui de sa mère\nC) Celui de ses frères\nD) Celui de ses cousins\nRéponse correcte: B) Celui de sa mère\nExplication: La figure maternelle occupe une place centrale dans les souvenirs du condamné, symbolisant l'amour et la tendresse."
            },
            {
                "id": "ch2_q16",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "difficile",
                "theme_semantique": "universalite_souffrance",
                "prefixe": "générer une question:",
                "texte_entree": "La souffrance du condamné, bien que spécifique, touche à des questions universelles sur la mort et la condition humaine.",
                "texte_cible": "Pourquoi la souffrance du condamné dépasse-t-elle son cas particulier ?\nA) Elle est très intense\nB) Elle touche à des questions universelles sur la mort\nC) Elle est bien décrite\nD) Elle est unique\nRéponse correcte: B) Elle touche à des questions universelles sur la mort\nExplication: La souffrance du condamné transcende son cas particulier pour aborder des questions universelles sur la mort et la condition humaine."
            },
            {
                "id": "ch2_q17",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "regrets_choix",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné passe en revue les choix de sa vie, se demandant lesquels l'ont mené à sa condamnation actuelle.",
                "texte_cible": "Que fait le condamné avec les choix de sa vie ?\nA) Il les oublie\nB) Il les passe en revue pour comprendre sa situation\nC) Il les invente\nD) Il les raconte aux gardiens\nRéponse correcte: B) Il les passe en revue pour comprendre sa situation\nExplication: Le condamné revisite ses choix passés pour tenter de comprendre l'enchaînement qui l'a mené à sa condamnation."
            },
            {
                "id": "ch2_q18",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "moyen",
                "theme_semantique": "psychologie_trauma",
                "prefixe": "générer une question:",
                "texte_entree": "La condamnation à mort crée un traumatisme psychologique profond chez le condamné, affectant sa perception du temps et de la réalité.",
                "texte_cible": "Quel effet produit la condamnation à mort sur la psychologie du condamné ?\nA) Elle le rend plus fort\nB) Elle crée un traumatisme psychologique profond\nC) Elle l'indiffère\nD) Elle le rend joyeux\nRéponse correcte: B) Elle crée un traumatisme psychologique profond\nExplication: La condamnation à mort provoque un traumatisme psychologique majeur qui altère la perception du condamné."
            },
            {
                "id": "ch2_q19",
                "chapitre": 2,
                "type": "comprehension",
                "difficulte": "facile",
                "theme_semantique": "angoisse_avenir",
                "prefixe": "générer une question:",
                "texte_entree": "Le condamné est obsédé par l'idée de son exécution imminente, ne pouvant penser à autre chose.",
                "texte_cible": "De quoi le condamné est-il obsédé ?\nA) De sa famille\nB) De son exécution imminente\nC) De ses souvenirs\nD) De sa nourriture\nRéponse correcte: B) De son exécution imminente\nExplication: L'idée de son exécution imminente obsède complètement le condamné, envahissant toutes ses pensées."
            },
            {
                "id": "ch2_q20",
                "chapitre": 2,
                "type": "analyse",
                "difficulte": "difficile",
                "theme_semantique": "style_interieur",
                "prefixe": "générer une question:",
                "texte_entree": "Le style de Victor Hugo dans ce chapitre privilégie le monologue intérieur pour créer une intimité maximale avec le lecteur.",
                "texte_cible": "Quelle technique stylistique utilise Victor Hugo dans ce chapitre ?\nA) Le dialogue\nB) Le monologue intérieur\nC) La description\nD) L'action\nRéponse correcte: B) Le monologue intérieur\nExplication: Victor Hugo utilise le monologue intérieur pour créer une intimité maximale entre le lecteur et les pensées du condamné."
            }
        ]
    }
    
    # Ajouter les questions supplémentaires
    questions = data["dataset_entrainement_complet"]
    
    # Trouver où insérer les nouvelles questions pour le chapitre 2
    ch2_start = None
    for i, q in enumerate(questions):
        if q["chapitre"] == 2 and q["id"] == "ch2_q1":
            ch2_start = i
            break
    
    if ch2_start is not None:
        # Insérer les nouvelles questions après ch2_q4
        ch2_q4_end = ch2_start + 4  # ch2_q1, ch2_q2, ch2_q3, ch2_q4
        for i, new_q in enumerate(additional_questions[2]):
            questions.insert(ch2_q4_end + i, new_q)
    
    # Mettre à jour le nombre d'exemples
    data["metadata"]["nombre_exemples"] = len(questions)
    data["metadata"]["version"] = "2.0_enriched"
    
    # Sauvegarder le fichier enrichi
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fichier enrichi avec succès !")
    print(f"📊 Nombre total de questions: {len(questions)}")
    print(f"📊 Questions chapitre 1: {len([q for q in questions if q['chapitre'] == 1])}")
    print(f"📊 Questions chapitre 2: {len([q for q in questions if q['chapitre'] == 2])}")

if __name__ == "__main__":
    enrich_questions()





