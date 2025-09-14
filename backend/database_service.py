import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self.connection = None
        
    def get_connection(self):
        """Obtenir une connexion à la base de données"""
        try:
            if self.connection is None:
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row  # Permet l'accès par nom de colonne
            return self.connection
        except Exception as e:
            logger.error(f"❌ Erreur de connexion à la base: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Exécuter une requête SQL et retourner les résultats"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            else:
                conn.commit()
                return [{"affected_rows": cursor.rowcount}]
                
        except Exception as e:
            logger.error(f"❌ Erreur d'exécution de requête: {e}")
            logger.error(f"Requête: {query}")
            logger.error(f"Paramètres: {params}")
            raise
    
    def get_real_student_performances(self) -> List[Dict[str, Any]]:
        """Récupérer les vraies performances des étudiants depuis la base"""
        query = """
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            COUNT(qr.id) as testsCompleted,
            AVG(qr.score) as averageScore,
            MAX(qr.created_at) as lastTestDate
        FROM users u
        LEFT JOIN analytics_results qr ON u.id = qr.user_id
        WHERE u.role = 'student'
        GROUP BY u.id, u.first_name, u.last_name, u.email
        HAVING testsCompleted > 0
        ORDER BY averageScore DESC
        """
        
        try:
            results = self.execute_query(query)
            logger.info(f"✅ {len(results)} étudiants récupérés depuis la vraie base")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des étudiants: {e}")
            return []
    
    def get_real_test_performances(self) -> List[Dict[str, Any]]:
        """Récupérer les vraies performances des tests depuis la base"""
        query = """
        SELECT 
            q.id,
            q.title,
            q.subject,
            COUNT(qr.id) as participants,
            AVG(qr.score) as averageScore,
            COUNT(CASE WHEN qr.score >= 70 THEN 1 END) * 100.0 / COUNT(qr.id) as completionRate,
            q.difficulty_level as difficultyLevel,
            AVG(qr.time_spent) as timeSpent,
            COUNT(CASE WHEN qr.score >= 60 THEN 1 END) * 100.0 / COUNT(qr.id) as successRate,
            MAX(qr.created_at) as lastAttemptDate
        FROM analytics_quizzes q
        LEFT JOIN analytics_results qr ON q.id = qr.quiz_id
        WHERE qr.id IS NOT NULL
        GROUP BY q.id, q.title, q.subject, q.difficulty_level
        HAVING participants > 0
        ORDER BY averageScore DESC
        """
        
        try:
            results = self.execute_query(query)
            logger.info(f"✅ {len(results)} tests récupérés depuis la vraie base")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des tests: {e}")
            return []
    
    def get_real_weekly_progress(self) -> List[Dict[str, Any]]:
        """Récupérer le progrès hebdomadaire réel depuis la base"""
        query = """
        SELECT 
            strftime('%W', qr.created_at) as week,
            AVG(qr.score) as averageScore,
            COUNT(qr.id) as testsCompleted,
            COUNT(DISTINCT qr.user_id) as studentsActive
        FROM analytics_results qr
        WHERE qr.created_at >= date('now', '-7 weeks')
        GROUP BY strftime('%W', qr.created_at)
        ORDER BY week ASC
        """
        
        try:
            results = self.execute_query(query)
            logger.info(f"✅ Progrès hebdomadaire récupéré depuis la vraie base")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération du progrès: {e}")
            return []
    
    def get_real_monthly_stats(self) -> List[Dict[str, Any]]:
        """Récupérer les statistiques mensuelles réelles depuis la base"""
        query = """
        SELECT 
            strftime('%m', qr.created_at) as month,
            COUNT(DISTINCT q.id) as testsCreated,
            COUNT(DISTINCT qr.user_id) as studentsActive,
            AVG(qr.score) as averageScore
        FROM analytics_results qr
        JOIN analytics_quizzes q ON qr.quiz_id = q.id
        WHERE qr.created_at >= date('now', '-6 months')
        GROUP BY strftime('%m', qr.created_at)
        ORDER BY month ASC
        """
        
        try:
            results = self.execute_query(query)
            logger.info(f"✅ Statistiques mensuelles récupérées depuis la vraie base")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des stats: {e}")
            return []
    
    def get_student_learning_history(self, student_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Récupérer l'historique d'apprentissage d'un étudiant"""
        query = """
        SELECT 
            qr.created_at,
            qr.score,
            q.title,
            q.subject,
            qr.time_spent
        FROM analytics_results qr
        JOIN analytics_quizzes q ON qr.quiz_id = q.id
        WHERE qr.user_id = ? AND qr.created_at >= date('now', '-{} days')
        ORDER BY qr.created_at DESC
        """.format(days)
        
        try:
            results = self.execute_query(query, (student_id,))
            logger.info(f"✅ Historique de l'étudiant {student_id} récupéré")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération de l'historique: {e}")
            return []
    
    def get_subject_performance_trends(self, subject: str, days: int = 90) -> List[Dict[str, Any]]:
        """Récupérer les tendances de performance par matière"""
        query = """
        SELECT 
            strftime('%Y-%m-%d', qr.created_at) as date,
            AVG(qr.score) as averageScore,
            COUNT(qr.id) as attempts,
            COUNT(DISTINCT qr.user_id) as uniqueStudents
        FROM analytics_results qr
        JOIN analytics_quizzes q ON qr.quiz_id = q.id
        WHERE q.subject = ? AND qr.created_at >= date('now', '-{} days')
        GROUP BY strftime('%Y-%m-%d', qr.created_at)
        ORDER BY date ASC
        """.format(days)
        
        try:
            results = self.execute_query(query, (subject,))
            logger.info(f"✅ Tendances de la matière {subject} récupérées")
            return results
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des tendances: {e}")
            return []
    
    def close_connection(self):
        """Fermer la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("✅ Connexion à la base fermée")

# Instance globale du service
db_service = DatabaseService()
