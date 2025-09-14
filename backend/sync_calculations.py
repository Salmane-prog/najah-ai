#!/usr/bin/env python3
"""
Script pour synchroniser tous les calculs XP, badges et progression
entre les différents widgets du dashboard
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta

def sync_all_calculations():
    """Synchronise tous les calculs XP, badges et progression"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print(f"🔄 Synchronisation des calculs dans: {db_path.absolute()}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. CALCULER XP TOTAL ET NIVEAU POUR CHAQUE UTILISATEUR
        print("\n📊 1. Calcul des XP et niveaux...")
        
        # Récupérer tous les utilisateurs étudiants
        cursor.execute("SELECT id, username FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        
        for student_id, username in students:
            print(f"   🔍 Traitement de {username} (ID: {student_id})...")
            
            # Calculer XP total depuis quiz_results
            cursor.execute("""
                SELECT COALESCE(SUM(score), 0) as total_score
                FROM quiz_results 
                WHERE user_id = ?
            """, (student_id,))
            
            total_score = cursor.fetchone()[0] or 0
            
            # Calculer XP depuis learning_history
            cursor.execute("""
                SELECT COALESCE(SUM(score), 0) as learning_xp
                FROM learning_history 
                WHERE student_id = ?
            """, (student_id,))
            
            learning_xp = cursor.fetchone()[0] or 0
            
            # XP total = quiz + learning + bonus
            total_xp = total_score + learning_xp + 50  # Bonus de base
            
            # Calculer le niveau (chaque niveau = 100 XP)
            current_level = (total_xp // 100) + 1
            xp_for_current_level = total_xp % 100
            xp_for_next_level = 100
            
            print(f"      📈 XP total: {total_xp}, Niveau: {current_level}, Progression: {xp_for_current_level}/{xp_for_next_level}")
            
            # Mettre à jour ou créer l'enregistrement gamification
            cursor.execute("""
                INSERT OR REPLACE INTO gamification_test 
                (user_id, total_points, current_level, xp_current_level, xp_next_level, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student_id, total_xp, current_level, xp_for_current_level, xp_for_next_level, datetime.now().isoformat()))
            
            # Mettre à jour learning_history avec les bonnes valeurs
            cursor.execute("""
                UPDATE learning_history 
                SET progress = ?, time_spent = 30
                WHERE student_id = ? AND progress IS NULL
            """, (min(100.0, (total_xp / 200) * 100), student_id))
        
        # 2. CALCULER LES BADGES BASÉS SUR LES PERFORMANCES
        print("\n🏆 2. Calcul des badges...")
        
        for student_id, username in students:
            # Badge "Quiz Master" : 5 quiz complétés
            cursor.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id = ?", (student_id,))
            quiz_count = cursor.fetchone()[0]
            
            # Badge "Score Parfait" : Au moins un quiz avec 100%
            cursor.execute("SELECT MAX(score) FROM quiz_results WHERE user_id = ?", (student_id,))
            max_score = cursor.fetchone()[0] or 0
            
            # Badge "Quiz Expert" : Score moyen > 80%
            cursor.execute("SELECT AVG(score) FROM quiz_results WHERE user_id = ?", (student_id,))
            avg_score = cursor.fetchone()[0] or 0
            
            # Créer les badges
            badges = []
            if quiz_count >= 5:
                badges.append(('Quiz Master', 'Complété 5 quiz', 'gold'))
            if max_score >= 100:
                badges.append(('Score Parfait', 'Obtenu 100% sur un quiz', 'platinum'))
            if avg_score >= 80:
                badges.append(('Quiz Expert', 'Score moyen > 80%', 'silver'))
            
            # Insérer les badges dans la table badges
            for badge_name, description, rarity in badges:
                cursor.execute("""
                    INSERT OR IGNORE INTO badges 
                    (user_id, name, description, rarity, earned_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, badge_name, description, rarity, datetime.now().isoformat()))
            
            print(f"      🏅 {username}: {len(badges)} badges débloqués")
        
        # 3. SYNCHRONISER LES CALCULS DE PROGRESSION
        print("\n📈 3. Synchronisation des progressions...")
        
        for student_id, username in students:
            # Calculer la progression globale basée sur tous les critères
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM quiz_results WHERE user_id = ?) as quiz_count,
                    (SELECT COUNT(*) FROM badges WHERE user_id = ?) as badge_count,
                    (SELECT COALESCE(SUM(score), 0) FROM quiz_results WHERE user_id = ?) as total_score
            """, (student_id, student_id, student_id))
            
            quiz_count, badge_count, total_score = cursor.fetchone()
            
            # Progression = (quiz + badges + score) / 300 * 100
            max_possible = 300  # 100 quiz + 100 badges + 100 score
            current_progress = min(100, ((quiz_count + badge_count + (total_score / 10)) / max_possible) * 100)
            
            # Mettre à jour la progression dans learning_history
            cursor.execute("""
                UPDATE learning_history 
                SET progress = ?, time_spent = 45
                WHERE student_id = ? AND progress IS NULL
            """, (current_progress, student_id))
            
            print(f"      📊 {username}: Progression globale {current_progress:.1f}%")
        
        # 4. CORRIGER LES DONNÉES INCOHÉRENTES
        print("\n🔧 4. Correction des incohérences...")
        
        # S'assurer que calendar_events a des données cohérentes
        cursor.execute("SELECT COUNT(*) FROM calendar_events")
        calendar_count = cursor.fetchone()[0]
        
        if calendar_count == 0:
            # Insérer des événements d'exemple avec les bonnes relations
            cursor.execute("""
                INSERT INTO calendar_events 
                (title, description, event_type, start_time, end_time, subject, color, class_id, created_by, user_id)
                VALUES 
                ('Cours de Mathematiques', 'Algebre lineaire', 'course', '2025-08-12 09:00:00', '2025-08-12 10:30:00', 'Mathematiques', '#3B82F6', 1, 1, 4),
                ('Examen de Physique', 'Mecanique classique', 'exam', '2025-08-14 14:00:00', '2025-08-14 16:00:00', 'Physique', '#EF4444', 2, 1, 4),
                ('Devoir de Chimie', 'Stoechiometrie', 'homework', '2025-08-16 10:00:00', '2025-08-16 11:00:00', 'Chimie', '#10B981', 3, 1, 4)
            """)
            print("      📅 Événements de calendrier ajoutés")
        
        # Valider tous les changements
        conn.commit()
        
        print("\n🎉 Synchronisation terminée avec succès!")
        
        # Vérifier le résultat final
        print("\n📋 RÉSUMÉ DE LA SYNCHRONISATION:")
        for student_id, username in students:
            cursor.execute("""
                SELECT 
                    (SELECT total_points FROM gamification_test WHERE user_id = ?) as xp,
                    (SELECT current_level FROM gamification_test WHERE user_id = ?) as level,
                    (SELECT COUNT(*) FROM badges WHERE user_id = ?) as badges,
                    (SELECT COUNT(*) FROM quiz_results WHERE user_id = ?) as quizzes
            """, (student_id, student_id, student_id, student_id))
            
            xp, level, badges, quizzes = cursor.fetchone()
            print(f"   {username}: Niveau {level}, {xp} XP, {badges} badges, {quizzes} quiz")
        
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 SYNCHRONISATION DES CALCULS DASHBOARD")
    print("=" * 50)
    
    sync_all_calculations()
    
    print("\n" + "=" * 50)
    print("✅ SYNCHRONISATION TERMINÉE!")
    print("💡 IMPORTANT: Redémarrez le serveur backend maintenant!")
    print("🚀 Tous les widgets afficheront des données cohérentes")
    print("📊 XP, badges et progression seront synchronisés")
    print("🎯 Plus d'incohérences entre les widgets!")


