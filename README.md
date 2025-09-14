# 🚀 Najah AI - Système d'Analytics Éducative

## 📋 Description

**Najah AI** est une plateforme d'analytics éducative en temps réel avec système de remédiation intelligent. Elle permet de suivre les performances des étudiants, générer des rapports détaillés et proposer des solutions de remédiation personnalisées.

## 🛠️ Technologies

### Frontend
- **Next.js 15.4.1** - Framework React
- **React 19.1.0** - Bibliothèque UI
- **TypeScript** - Langage de programmation
- **Tailwind CSS** - Framework CSS
- **Chart.js** - Graphiques et visualisations

### Backend
- **FastAPI** - Framework Python
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de données
- **Redis** - Cache (optionnel)
- **Celery** - Tâches asynchrones

## 🚀 Déploiement

### Frontend (Vercel)
```bash
# Cloner le repository
git clone https://github.com/votre-username/najah-ai.git
cd najah-ai

# Installer les dépendances
cd frontend
npm install

# Démarrer en développement
npm run dev

# Build pour la production
npm run build
```

### Backend (Railway/AlwaysData)
```bash
# Installer les dépendances Python
cd backend
pip install -r requirements.txt

# Démarrer le serveur
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📁 Structure du projet

```
najah-ai/
├── frontend/                 # Application Next.js
│   ├── src/
│   │   ├── app/             # Pages et composants
│   │   ├── components/      # Composants réutilisables
│   │   └── lib/            # Utilitaires
│   ├── package.json
│   └── next.config.js
├── backend/                 # API FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── api_router.py
├── data/                    # Données et uploads
│   ├── app.db
│   └── uploads/
└── README.md
```

## 🔧 Configuration

### Variables d'environnement

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://votre-backend-url.com
NEXT_PUBLIC_APP_NAME=Najah AI
NODE_ENV=production
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=https://votre-frontend-url.com
PYTHON_ENV=production
```

## 📊 Fonctionnalités

- **Dashboard Analytics** - Tableaux de bord en temps réel
- **Suivi des performances** - Suivi des étudiants et tests
- **Rapports détaillés** - Génération de rapports PDF/Excel
- **Système de remédiation** - Suggestions personnalisées
- **Authentification** - Gestion des utilisateurs et rôles
- **API REST** - Endpoints pour intégrations

## 🚀 Déploiement rapide

### Vercel (Frontend)
1. Connecter votre repository GitHub à Vercel
2. Vercel détecte automatiquement Next.js
3. Déploiement automatique en quelques secondes

### Railway (Backend)
1. Connecter votre repository GitHub à Railway
2. Railway détecte automatiquement Python/FastAPI
3. Configuration automatique de PostgreSQL

## 📱 URLs de déploiement

- **Frontend** : https://najah-ai.vercel.app
- **Backend API** : https://najah-ai-backend.railway.app
- **Documentation API** : https://najah-ai-backend.railway.app/docs

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Équipe

- **Développeur Principal** : [Votre nom]
- **Email** : [votre-email@example.com]

## 📞 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Najah AI** - Révolutionner l'analytics éducative avec l'IA 🎓✨