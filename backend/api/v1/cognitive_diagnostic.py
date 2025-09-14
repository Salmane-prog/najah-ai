from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.quiz import QuizResult, Quiz
from models.learning_history import LearningHistory
from api.v1.auth import require_role, get_current_user
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from models.user import UserRole

router = APIRouter()

@router.get("/student/{student_id}/profile")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer le profil d'un étudiant (pour compatibilité frontend)"""
    try:
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Déterminer le nom à afficher
        display_name = "Élève sans nom"
        if student.first_name and student.last_name:
            display_name = f"{student.first_name} {student.last_name}"
        elif student.username:
            display_name = student.username
        elif student.email:
            email_name = student.email.split('@')[0]
            display_name = email_name.replace('.', ' ').title()
        
        return {
            "id": student.id,
            "name": display_name,
            "email": student.email,
            "role": student.role.value,
            "avatar_url": student.avatar,
            "bio": student.bio,
            "phone": student.phone
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Erreur dans get_student_profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du profil étudiant: {str(e)}"
        )

@router.get("/class/{class_id}/cognitive-analysis")
def get_class_cognitive_analysis(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Analyser les profils cognitifs d'une classe."""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        student_ids = [cs.student_id for cs in class_students]
        
        if not student_ids:
            return {"message": "Aucun étudiant dans cette classe", "analysis": {}}
        
        # Analyser chaque étudiant
        student_profiles = []
        learning_styles_distribution = {}
        
        for student_id in student_ids:
            profile = get_cognitive_profile(student_id, db, current_user)
            student_profiles.append(profile)
            
            # Compter les styles d'apprentissage
            style = profile.get("learning_style", {}).get("primary_style", "unknown")
            learning_styles_distribution[style] = learning_styles_distribution.get(style, 0) + 1
        
        # Analyser les patterns de classe
        class_patterns = analyze_class_cognitive_patterns(student_profiles)
        
        return {
            "class_id": class_id,
            "analysis_date": datetime.utcnow().isoformat(),
            "students_analyzed": len(student_ids),
            "learning_styles_distribution": learning_styles_distribution,
            "class_patterns": class_patterns,
            "teaching_recommendations": generate_class_teaching_recommendations(class_patterns, learning_styles_distribution)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse cognitive classe: {str(e)}")

@router.post("/student/{student_id}/learning-style-assessment")
def assess_learning_style(
    student_id: int,
    assessment_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Évaluer le style d'apprentissage d'un étudiant via un questionnaire."""
    try:
        # Analyser les réponses du questionnaire
        style_scores = analyze_learning_style_assessment(assessment_data)
        
        # Déterminer le style dominant
        primary_style = determine_primary_learning_style(style_scores)
        
        # Générer des recommandations basées sur le style
        style_recommendations = generate_style_based_recommendations(primary_style, style_scores)
        
        # Sauvegarder l'évaluation
        save_learning_style_assessment(student_id, style_scores, primary_style, db)
        
        return {
            "student_id": student_id,
            "assessment_date": datetime.utcnow().isoformat(),
            "primary_style": primary_style,
            "style_scores": style_scores,
            "recommendations": style_recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur évaluation style d'apprentissage: {str(e)}")

def analyze_learning_patterns(student_id: int, db: Session) -> Dict[str, Any]:
    """Analyser les patterns d'apprentissage d'un étudiant."""
    # Récupérer l'historique d'apprentissage
    learning_history = db.query(LearningHistory).filter(
        LearningHistory.student_id == student_id
    ).order_by(LearningHistory.timestamp.desc()).limit(100).all()
    
    if not learning_history:
        return {"message": "Données d'apprentissage insuffisantes"}
    
    # Analyser les heures d'activité
    hour_activity = {}
    for session in learning_history:
        hour = session.timestamp.hour
        hour_activity[hour] = hour_activity.get(hour, 0) + 1
    
    # Analyser la durée des sessions
    session_durations = [s.time_spent for s in learning_history if s.time_spent]
    avg_duration = sum(session_durations) / len(session_durations) if session_durations else 0
    
    # Analyser les types d'activités
    activity_types = {}
    for session in learning_history:
        activity_type = session.action or "unknown"
        activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
    
    # Analyser la fréquence d'apprentissage
    daily_activity = {}
    for session in learning_history:
        day = session.timestamp.strftime('%Y-%m-%d')
        daily_activity[day] = daily_activity.get(day, 0) + 1
    
    return {
        "total_sessions": len(learning_history),
        "peak_hours": sorted(hour_activity.items(), key=lambda x: x[1], reverse=True)[:3],
        "average_session_duration": round(avg_duration, 2),
        "preferred_activity_types": sorted(activity_types.items(), key=lambda x: x[1], reverse=True)[:5],
        "learning_frequency": len(daily_activity),
        "consistency_score": calculate_learning_consistency(daily_activity)
    }

def determine_learning_style(patterns: Dict) -> Dict[str, Any]:
    """Déterminer le style d'apprentissage dominant."""
    if "message" in patterns:
        return {"primary_style": "unknown", "confidence": "low"}
    
    # Analyser les patterns pour déterminer le style
    peak_hours = patterns.get("peak_hours", [])
    avg_duration = patterns.get("average_session_duration", 0)
    activity_types = patterns.get("preferred_activity_types", [])
    consistency = patterns.get("consistency_score", 0)
    
    # Logique de détermination du style
    style_indicators = {
        "visual": 0,
        "auditory": 0,
        "kinesthetic": 0,
        "reading_writing": 0
    }
    
    # Analyser les heures de pointe
    if peak_hours:
        morning_hours = sum(1 for hour, _ in peak_hours if 6 <= hour <= 12)
        afternoon_hours = sum(1 for hour, _ in peak_hours if 12 < hour <= 18)
        evening_hours = sum(1 for hour, _ in peak_hours if 18 < hour <= 23)
        
        if morning_hours > afternoon_hours and morning_hours > evening_hours:
            style_indicators["visual"] += 2  # Les apprenants visuels préfèrent souvent le matin
        elif evening_hours > morning_hours and evening_hours > afternoon_hours:
            style_indicators["auditory"] += 2  # Les apprenants auditifs peuvent préférer le soir
    
    # Analyser la durée des sessions
    if avg_duration > 45:
        style_indicators["kinesthetic"] += 2  # Sessions longues = kinesthésique
    elif avg_duration < 20:
        style_indicators["visual"] += 1  # Sessions courtes = visuel
    
    # Analyser les types d'activités
    for activity_type, count in activity_types:
        if "quiz" in activity_type.lower():
            style_indicators["reading_writing"] += 1
        elif "video" in activity_type.lower() or "content" in activity_type.lower():
            style_indicators["visual"] += 1
        elif "audio" in activity_type.lower():
            style_indicators["auditory"] += 1
        elif "interactive" in activity_type.lower():
            style_indicators["kinesthetic"] += 1
    
    # Déterminer le style dominant
    primary_style = max(style_indicators.items(), key=lambda x: x[1])[0]
    confidence = "high" if style_indicators[primary_style] >= 3 else "medium" if style_indicators[primary_style] >= 1 else "low"
    
    return {
        "primary_style": primary_style,
        "style_scores": style_indicators,
        "confidence": confidence,
        "secondary_styles": [style for style, score in sorted(style_indicators.items(), key=lambda x: x[1], reverse=True)[1:3]]
    }

def analyze_cognitive_strengths_weaknesses(student_id: int, db: Session) -> Dict[str, Any]:
    """Analyser les forces et faiblesses cognitives."""
    # Récupérer les résultats de quiz
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id
    ).order_by(QuizResult.created_at.desc()).limit(50).all()
    
    if not quiz_results:
        return {"message": "Données de performance insuffisantes"}
    
    # Analyser par sujet
    subject_performance = {}
    for result in quiz_results:
        subject = result.sujet or "Général"
        if subject not in subject_performance:
            subject_performance[subject] = []
        subject_performance[subject].append(result.score)
    
    # Identifier les forces et faiblesses
    strengths = []
    weaknesses = []
    
    for subject, scores in subject_performance.items():
        avg_score = sum(scores) / len(scores)
        if avg_score >= 80:
            strengths.append({
                "subject": subject,
                "average_score": round(avg_score, 2),
                "consistency": calculate_score_consistency(scores)
            })
        elif avg_score < 60:
            weaknesses.append({
                "subject": subject,
                "average_score": round(avg_score, 2),
                "consistency": calculate_score_consistency(scores)
            })
    
    # Analyser les patterns cognitifs
    cognitive_patterns = analyze_cognitive_patterns(quiz_results)
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "cognitive_patterns": cognitive_patterns,
        "overall_performance": round(sum(r.score for r in quiz_results) / len(quiz_results), 2)
    }

def analyze_cognitive_patterns(quiz_results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser les patterns cognitifs."""
    if not quiz_results:
        return {}
    
    # Analyser la vitesse de réponse (si disponible)
    response_times = []
    for result in quiz_results:
        if hasattr(result, 'time_spent') and result.time_spent:
            response_times.append(result.time_spent)
    
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Analyser la progression temporelle
    scores = [r.score for r in quiz_results]
    if len(scores) >= 5:
        recent_avg = sum(scores[:5]) / 5
        older_avg = sum(scores[5:10]) / 5 if len(scores) >= 10 else recent_avg
        learning_rate = recent_avg - older_avg
    else:
        learning_rate = 0
    
    # Analyser la variabilité des scores
    score_variance = calculate_score_variance(scores)
    
    return {
        "average_response_time": round(avg_response_time, 2),
        "learning_rate": round(learning_rate, 2),
        "score_variance": round(score_variance, 2),
        "cognitive_flexibility": "high" if score_variance < 200 else "medium" if score_variance < 400 else "low"
    }

def generate_cognitive_recommendations(learning_style: Dict, cognitive_analysis: Dict) -> List[str]:
    """Générer des recommandations basées sur l'analyse cognitive."""
    recommendations = []
    
    # Recommandations basées sur le style d'apprentissage
    primary_style = learning_style.get("primary_style", "unknown")
    
    if primary_style == "visual":
        recommendations.append("Privilégier les supports visuels (graphiques, diagrammes, vidéos)")
        recommendations.append("Utiliser des cartes mentales pour organiser l'information")
    elif primary_style == "auditory":
        recommendations.append("Écouter des podcasts ou des explications audio")
        recommendations.append("Participer à des discussions de groupe")
    elif primary_style == "kinesthetic":
        recommendations.append("Pratiquer avec des exercices interactifs")
        recommendations.append("Utiliser des simulations et des expériences pratiques")
    elif primary_style == "reading_writing":
        recommendations.append("Prendre des notes détaillées")
        recommendations.append("Résumer les informations par écrit")
    
    # Recommandations basées sur les forces et faiblesses
    if cognitive_analysis.get("strengths"):
        recommendations.append(f"Exploiter les forces en: {', '.join([s['subject'] for s in cognitive_analysis['strengths'][:3]])}")
    
    if cognitive_analysis.get("weaknesses"):
        recommendations.append(f"Renforcer les matières: {', '.join([w['subject'] for w in cognitive_analysis['weaknesses'][:3]])}")
    
    return recommendations

def calculate_profile_confidence(patterns: Dict) -> str:
    """Calculer le niveau de confiance du profil cognitif."""
    if "message" in patterns:
        return "low"
    
    total_sessions = patterns.get("total_sessions", 0)
    consistency = patterns.get("consistency_score", 0)
    
    if total_sessions >= 50 and consistency >= 70:
        return "high"
    elif total_sessions >= 20 and consistency >= 50:
        return "medium"
    else:
        return "low"

def analyze_learning_style_assessment(assessment_data: Dict) -> Dict[str, int]:
    """Analyser les réponses d'un questionnaire de style d'apprentissage."""
    # Logique simplifiée pour analyser les réponses
    style_scores = {
        "visual": 0,
        "auditory": 0,
        "kinesthetic": 0,
        "reading_writing": 0
    }
    
    # Analyser les réponses (exemple simplifié)
    for question_id, answer in assessment_data.items():
        if "visual" in question_id.lower():
            style_scores["visual"] += answer
        elif "audio" in question_id.lower():
            style_scores["auditory"] += answer
        elif "hands" in question_id.lower() or "practice" in question_id.lower():
            style_scores["kinesthetic"] += answer
        elif "read" in question_id.lower() or "write" in question_id.lower():
            style_scores["reading_writing"] += answer
    
    return style_scores

def determine_primary_learning_style(style_scores: Dict[str, int]) -> str:
    """Déterminer le style d'apprentissage principal."""
    return max(style_scores.items(), key=lambda x: x[1])[0]

def generate_style_based_recommendations(primary_style: str, style_scores: Dict[str, int]) -> List[str]:
    """Générer des recommandations basées sur le style d'apprentissage."""
    recommendations = []
    
    if primary_style == "visual":
        recommendations.extend([
            "Utiliser des graphiques et diagrammes",
            "Regarder des vidéos explicatives",
            "Créer des cartes mentales",
            "Utiliser des couleurs pour organiser l'information"
        ])
    elif primary_style == "auditory":
        recommendations.extend([
            "Écouter des podcasts éducatifs",
            "Participer à des discussions de groupe",
            "Répéter les informations à voix haute",
            "Utiliser des mnémoniques auditives"
        ])
    elif primary_style == "kinesthetic":
        recommendations.extend([
            "Pratiquer avec des exercices interactifs",
            "Utiliser des simulations",
            "Prendre des pauses fréquentes",
            "Associer l'apprentissage à des mouvements"
        ])
    elif primary_style == "reading_writing":
        recommendations.extend([
            "Prendre des notes détaillées",
            "Résumer les informations par écrit",
            "Créer des listes et des plans",
            "Lire des textes explicatifs"
        ])
    
    return recommendations

def save_learning_style_assessment(student_id: int, style_scores: Dict, primary_style: str, db: Session):
    """Sauvegarder l'évaluation du style d'apprentissage."""
    # Ici on pourrait sauvegarder dans une table dédiée
    # Pour l'instant, on utilise learning_history
    assessment_record = LearningHistory(
        student_id=student_id,
        action="learning_style_assessment",
        details=json.dumps({
            "style_scores": style_scores,
            "primary_style": primary_style,
            "assessment_date": datetime.utcnow().isoformat()
        }),
        timestamp=datetime.utcnow()
    )
    
    db.add(assessment_record)
    db.commit()

def analyze_class_cognitive_patterns(student_profiles: List[Dict]) -> Dict[str, Any]:
    """Analyser les patterns cognitifs d'une classe."""
    if not student_profiles:
        return {}
    
    # Analyser la distribution des styles
    style_distribution = {}
    for profile in student_profiles:
        primary_style = profile.get("learning_style", {}).get("primary_style", "unknown")
        style_distribution[primary_style] = style_distribution.get(primary_style, 0) + 1
    
    # Analyser les patterns communs
    common_strengths = []
    common_weaknesses = []
    
    for profile in student_profiles:
        cognitive_analysis = profile.get("cognitive_analysis", {})
        if cognitive_analysis.get("strengths"):
            common_strengths.extend([s["subject"] for s in cognitive_analysis["strengths"]])
        if cognitive_analysis.get("weaknesses"):
            common_weaknesses.extend([w["subject"] for w in cognitive_analysis["weaknesses"]])
    
    # Compter les occurrences
    from collections import Counter
    strength_counts = Counter(common_strengths)
    weakness_counts = Counter(common_weaknesses)
    
    return {
        "style_distribution": style_distribution,
        "common_strengths": strength_counts.most_common(3),
        "common_weaknesses": weakness_counts.most_common(3),
        "diversity_score": calculate_class_diversity(style_distribution)
    }

def generate_class_teaching_recommendations(class_patterns: Dict, style_distribution: Dict) -> List[str]:
    """Générer des recommandations d'enseignement pour la classe."""
    recommendations = []
    
    # Recommandations basées sur la distribution des styles
    dominant_style = max(style_distribution.items(), key=lambda x: x[1])[0] if style_distribution else "unknown"
    
    if dominant_style == "visual":
        recommendations.append("Privilégier les supports visuels en classe")
    elif dominant_style == "auditory":
        recommendations.append("Encourager les discussions et explications orales")
    elif dominant_style == "kinesthetic":
        recommendations.append("Intégrer des activités pratiques et interactives")
    elif dominant_style == "reading_writing":
        recommendations.append("Fournir des supports écrits détaillés")
    
    # Recommandations pour la diversité
    if len(style_distribution) >= 3:
        recommendations.append("Utiliser une approche multimodale pour couvrir tous les styles")
    
    # Recommandations basées sur les faiblesses communes
    if class_patterns.get("common_weaknesses"):
        recommendations.append(f"Renforcer l'enseignement de: {', '.join([w[0] for w in class_patterns['common_weaknesses'][:2]])}")
    
    return recommendations

def calculate_learning_consistency(daily_activity: Dict) -> float:
    """Calculer la cohérence de l'apprentissage."""
    if not daily_activity:
        return 0.0
    
    days = list(daily_activity.keys())
    if len(days) < 2:
        return 100.0
    
    # Calculer la variance de l'activité quotidienne
    activities = list(daily_activity.values())
    mean_activity = sum(activities) / len(activities)
    variance = sum((activity - mean_activity) ** 2 for activity in activities) / len(activities)
    
    # Plus la variance est faible, plus la cohérence est élevée
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2)

def calculate_score_consistency(scores: List[float]) -> float:
    """Calculer la cohérence des scores."""
    if len(scores) < 2:
        return 100.0
    
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    
    # Plus la variance est faible, plus la cohérence est élevée
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2)

def calculate_score_variance(scores: List[float]) -> float:
    """Calculer la variance des scores."""
    if len(scores) < 2:
        return 0.0
    
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    return variance

def calculate_class_diversity(style_distribution: Dict) -> float:
    """Calculer le score de diversité d'une classe."""
    if not style_distribution:
        return 0.0
    
    total_students = sum(style_distribution.values())
    if total_students == 0:
        return 0.0
    
    # Calculer l'entropie de Shannon pour mesurer la diversité
    entropy = 0
    for count in style_distribution.values():
        if count > 0:
            probability = count / total_students
            entropy -= probability * (probability.bit_length() - 1)  # log2 approximation
    
    # Normaliser entre 0 et 100
    max_entropy = (len(style_distribution) - 1).bit_length() - 1  # log2 du nombre de styles
    diversity_score = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
    
    return round(diversity_score, 2) 

def get_cognitive_profile(student_id: int, db: Session, current_user: User) -> Dict[str, Any]:
    """Récupérer le profil cognitif complet d'un étudiant."""
    try:
        # Analyser les patterns d'apprentissage
        learning_patterns = analyze_learning_patterns(student_id, db)
        
        # Déterminer le style d'apprentissage
        learning_style = determine_learning_style(learning_patterns)
        
        # Analyser les forces et faiblesses cognitives
        cognitive_analysis = analyze_cognitive_strengths_weaknesses(student_id, db)
        
        # Générer des recommandations
        recommendations = generate_cognitive_recommendations(learning_style, cognitive_analysis)
        
        # Calculer le niveau de confiance
        confidence = calculate_profile_confidence(learning_patterns)
        
        return {
            "student_id": student_id,
            "learning_patterns": learning_patterns,
            "learning_style": learning_style,
            "cognitive_analysis": cognitive_analysis,
            "recommendations": recommendations,
            "confidence": confidence
        }
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_cognitive_profile: {e}")
        return {"error": str(e)}

@router.get("/student/{student_id}/cognitive-profile")
def get_student_cognitive_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le profil cognitif complet d'un étudiant."""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Vérifier les permissions
        if current_user.role == UserRole.student and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les résultats de quiz pour analyser le profil cognitif
        from models.quiz import QuizResult
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).order_by(QuizResult.created_at.desc()).limit(50).all()
        
        if not quiz_results:
            raise HTTPException(status_code=404, detail="Aucune donnée suffisante pour le diagnostic cognitif")
        
        # Analyser les performances pour déterminer le style d'apprentissage
        total_score = sum(r.score for r in quiz_results)
        avg_score = total_score / len(quiz_results)
        
        # Analyser le temps de réponse moyen si disponible
        response_times = [r.time_spent for r in quiz_results if r.time_spent and r.time_spent > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 300  # 5 min par défaut
        
        # Déterminer le style d'apprentissage basé sur les performances
        learning_style = "Visuel"
        confidence_score = 0.6
        
        if avg_score >= 80:
            learning_style = "Analytique"
            confidence_score = 0.8
        elif avg_score >= 60:
            learning_style = "Auditif"
            confidence_score = 0.7
        elif avg_response_time < 180:  # Moins de 3 minutes
            learning_style = "Kinesthésique"
            confidence_score = 0.6
        
        # Calculer les capacités cognitives basées sur les performances réelles
        memory_strength = min(0.9, avg_score / 100)
        attention_span = min(0.9, max(0.3, (600 - avg_response_time) / 600))  # Basé sur le temps de concentration
        problem_solving = min(0.9, avg_score / 100)
        visual_processing = 0.6  # Valeur moyenne, pourrait être affinée avec plus de données
        auditory_processing = 0.7 if learning_style == "Auditif" else 0.5
        
        # Analyser les forces et faiblesses basées sur les sujets des quiz
        from collections import defaultdict
        subject_scores = defaultdict(list)
        
        for result in quiz_results:
            subject = result.sujet or "Général"
            subject_scores[subject].append(result.score)
        
        strengths = []
        areas_for_improvement = []
        
        for subject, scores in subject_scores.items():
            avg_subject_score = sum(scores) / len(scores)
            if avg_subject_score >= 75:
                strengths.append(f"Excellence en {subject}")
            elif avg_subject_score < 50:
                areas_for_improvement.append(f"Difficultés en {subject}")
        
        # Générer des recommandations basées sur les performances réelles
        recommendations = []
        if avg_score < 60:
            recommendations.append("Réviser les concepts fondamentaux")
        if avg_response_time > 400:  # Plus de 6 minutes
            recommendations.append("Améliorer la gestion du temps")
        if len(areas_for_improvement) > 0:
            recommendations.append(f"Se concentrer sur les domaines faibles: {', '.join(areas_for_improvement)}")
        
        return {
            "student_id": student_id,
            "learning_style": {
                "primary_style": learning_style,
                "confidence_score": confidence_score,
                "evidence": [f"Analyse de {len(quiz_results)} quiz", "Temps de réponse moyen", "Scores par matière"]
            },
            "cognitive_abilities": {
                "memory_strength": round(memory_strength, 2),
                "attention_span": round(attention_span, 2),
                "problem_solving": round(problem_solving, 2),
                "visual_processing": round(visual_processing, 2),
                "auditory_processing": round(auditory_processing, 2)
            },
            "learning_preferences": {
                "preferred_content_types": ["interactif", "visuel"] if learning_style == "Visuel" else ["audio", "texte"],
                "preferred_difficulty": "facile" if avg_score < 60 else "moyen" if avg_score < 80 else "difficile",
                "preferred_pace": "lent" if avg_response_time > 400 else "modéré" if avg_response_time > 200 else "rapide",
                "preferred_environment": "calme"
            },
            "strengths": strengths if strengths else ["Persévérance", "Engagement"],
            "areas_for_improvement": areas_for_improvement if areas_for_improvement else ["Gestion du temps"],
            "recommendations": recommendations if recommendations else ["Continuer les efforts actuels"],
            "last_updated": datetime.utcnow().isoformat(),
            "data_based_on": f"{len(quiz_results)} quiz complétés"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Erreur dans get_student_cognitive_profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du profil cognitif: {str(e)}"
        )

@router.get("/student/{student_id}/cognitive-profile-test")
def get_student_cognitive_profile_test(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer le profil cognitif complet d'un étudiant (version test sans auth)."""
    try:
        print(f"🔍 [COGNITIVE_DIAGNOSTIC] Début analyse cognitive pour étudiant {student_id}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            print(f"❌ [COGNITIVE_DIAGNOSTIC] Étudiant {student_id} non trouvé")
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        print(f"✅ [COGNITIVE_DIAGNOSTIC] Étudiant trouvé: {student.first_name} {student.last_name}")
        
        # Récupérer les données de base pour l'analyse
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).order_by(QuizResult.created_at.desc()).limit(50).all()
        
        print(f"📊 [COGNITIVE_DIAGNOSTIC] Résultats trouvés: {len(quiz_results)}")
        
        if not quiz_results:
            # Retourner des données par défaut si pas de résultats
            return {
                "student_id": student_id,
                "student_name": f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email,
                "learning_style": "unknown",
                "primary_style_percentage": 0,
                "cognitive_strengths": [],
                "cognitive_weaknesses": [],
                "confidence_score": 30,
                "recommendations": [
                    "Commencer par des quiz simples pour établir un profil",
                    "Participer à plus d'activités d'apprentissage",
                    "Explorer différents types de contenu éducatif"
                ],
                "analysis_date": datetime.utcnow().isoformat(),
                "message": "Données insuffisantes pour une analyse complète"
            }
        
        # Analyser les performances par sujet
        subject_performance = {}
        for result in quiz_results:
            subject = result.sujet or "Général"
            if subject not in subject_performance:
                subject_performance[subject] = []
            subject_performance[subject].append(result.score)
        
        print(f"📊 [COGNITIVE_DIAGNOSTIC] Sujets analysés: {list(subject_performance.keys())}")
        
        # Déterminer le style d'apprentissage basé sur les performances
        learning_style = determine_learning_style_from_performance(subject_performance)
        
        # Identifier les forces et faiblesses
        strengths = []
        weaknesses = []
        
        for subject, scores in subject_performance.items():
            avg_score = sum(scores) / len(scores)
            if avg_score >= 70:
                strengths.append(f"{subject} (Score moyen: {round(avg_score, 1)}%)")
            elif avg_score < 50:
                weaknesses.append(f"{subject} (Score moyen: {round(avg_score, 1)}%)")
        
        # Calculer le score de confiance
        confidence_score = min(85, max(30, len(quiz_results) * 2))
        
        # Générer des recommandations
        recommendations = generate_recommendations_from_analysis(learning_style, strengths, weaknesses)
        
        # Déterminer le nom d'affichage
        display_name = "Élève sans nom"
        if student.first_name and student.last_name:
            display_name = f"{student.first_name} {student.last_name}"
        elif student.username:
            display_name = student.username
        elif student.email:
            email_name = student.email.split('@')[0]
            display_name = email_name.replace('.', ' ').title()
        
        response_data = {
            "student_id": student_id,
            "student_name": display_name,
            "learning_style": learning_style,
            "primary_style_percentage": calculate_style_percentage_from_performance(subject_performance),
            "cognitive_strengths": strengths,
            "cognitive_weaknesses": weaknesses,
            "confidence_score": confidence_score,
            "recommendations": recommendations,
            "analysis_date": datetime.utcnow().isoformat(),
            "total_quizzes": len(quiz_results)
        }
        
        print(f"✅ [COGNITIVE_DIAGNOSTIC] Analyse terminée pour {display_name}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [COGNITIVE_DIAGNOSTIC] Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse cognitive: {str(e)}"
        )

def determine_learning_style_from_performance(subject_performance: Dict[str, List[float]]) -> str:
    """Déterminer le style d'apprentissage basé sur les performances."""
    if not subject_performance:
        return "unknown"
    
    # Analyser les patterns de performance
    total_subjects = len(subject_performance)
    high_performance_subjects = sum(1 for scores in subject_performance.values() if sum(scores) / len(scores) >= 70)
    low_performance_subjects = sum(1 for scores in subject_performance.values() if sum(scores) / len(scores) < 50)
    
    # Déterminer le style basé sur les patterns
    if high_performance_subjects >= total_subjects * 0.7:
        return "visual"  # Bonnes performances = style visuel
    elif low_performance_subjects >= total_subjects * 0.5:
        return "kinesthetic"  # Performances faibles = besoin de pratique
    else:
        return "auditory"  # Performance mixte = style auditif

def calculate_style_percentage_from_performance(subject_performance: Dict[str, List[float]]) -> int:
    """Calculer le pourcentage du style basé sur les performances."""
    if not subject_performance:
        return 0
    
    total_subjects = len(subject_performance)
    high_performance_count = sum(1 for scores in subject_performance.values() if sum(scores) / len(scores) >= 70)
    
    return round((high_performance_count / total_subjects) * 100)

def generate_recommendations_from_analysis(learning_style: str, strengths: List[str], weaknesses: List[str]) -> List[str]:
    """Générer des recommandations basées sur l'analyse."""
    recommendations = []
    
    # Recommandations basées sur le style d'apprentissage
    if learning_style == "visual":
        recommendations.extend([
            "Utiliser des graphiques et diagrammes pour l'apprentissage",
            "Regarder des vidéos explicatives",
            "Créer des cartes mentales pour organiser l'information"
        ])
    elif learning_style == "auditory":
        recommendations.extend([
            "Écouter des podcasts éducatifs",
            "Participer à des discussions de groupe",
            "Répéter les informations à voix haute"
        ])
    elif learning_style == "kinesthetic":
        recommendations.extend([
            "Pratiquer avec des exercices interactifs",
            "Utiliser des simulations et expériences pratiques",
            "Prendre des pauses fréquentes pendant l'apprentissage"
        ])
    else:
        recommendations.extend([
            "Explorer différents styles d'apprentissage",
            "Tester différentes méthodes d'étude",
            "Demander de l'aide pour identifier le style optimal"
        ])
    
    # Recommandations basées sur les forces
    if strengths:
        recommendations.append(f"Exploiter les forces en: {', '.join(strengths[:2])}")
    
    # Recommandations basées sur les faiblesses
    if weaknesses:
        recommendations.append(f"Travailler sur: {', '.join(weaknesses[:2])}")
    
    return recommendations

def calculate_style_percentage(learning_style: Dict) -> int:
    """Calculer le pourcentage du style principal."""
    style_scores = learning_style.get("style_scores", {})
    if not style_scores:
        return 0
    
    primary_style = learning_style.get("primary_style", "unknown")
    primary_score = style_scores.get(primary_style, 0)
    total_score = sum(style_scores.values())
    
    if total_score == 0:
        return 0
    
    return round((primary_score / total_score) * 100)

def format_cognitive_strengths(cognitive_analysis: Dict) -> List[str]:
    """Formater les forces cognitives pour l'affichage."""
    strengths = cognitive_analysis.get("strengths", [])
    if not strengths:
        return []
    
    return [f"{s['subject']} (Score moyen: {s['average_score']}%)" for s in strengths[:5]]

def format_cognitive_weaknesses(cognitive_analysis: Dict) -> List[str]:
    """Formater les faiblesses cognitives pour l'affichage."""
    weaknesses = cognitive_analysis.get("weaknesses", [])
    if not weaknesses:
        return []
    
    return [f"{w['subject']} (Score moyen: {w['average_score']}%)" for w in weaknesses[:5]]

def calculate_confidence_score(confidence: str) -> int:
    """Convertir le niveau de confiance en score numérique."""
    confidence_map = {
        "high": 85,
        "medium": 60,
        "low": 30
    }
    return confidence_map.get(confidence, 30) 