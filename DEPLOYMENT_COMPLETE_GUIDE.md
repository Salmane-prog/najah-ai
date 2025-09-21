# 🚀 Guide de Déploiement Complet - Najah AI

## 📋 Vue d'ensemble

**Najah AI** est une plateforme d'analytics éducative full-stack avec :
- **Frontend** : Next.js 15.4.1 + React 19.1.0 + TypeScript
- **Backend** : FastAPI + Python + SQLite/PostgreSQL
- **Fonctionnalités** : Dashboard analytics, système de remédiation, authentification

---

## 🎯 **Option 1 : Déploiement Rapide (Vercel + Railway) - RECOMMANDÉE**

### **Avantages** :
- ✅ Gratuit pour commencer
- ✅ Déploiement automatique
- ✅ Optimisé pour Next.js
- ✅ Base de données gérée

### **Étapes de déploiement** :

#### **1. Préparer le Frontend**

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Tester le build
npm run build

# Vérifier que tout fonctionne
npm run start
```

#### **2. Déployer le Frontend sur Vercel**

1. **Aller sur [vercel.com](https://vercel.com)**
2. **Se connecter avec GitHub**
3. **Importer le repository**
4. **Configuration** :
   - **Framework Preset** : Next.js
   - **Root Directory** : `frontend`
   - **Build Command** : `npm run build`
   - **Output Directory** : `.next`

5. **Variables d'environnement** :
   ```
   NEXT_PUBLIC_API_URL=https://votre-backend-railway-url.com
   NEXT_PUBLIC_APP_NAME=Najah AI
   ```

#### **3. Déployer le Backend sur Railway**

1. **Aller sur [railway.app](https://railway.app)**
2. **Se connecter avec GitHub**
3. **Créer un nouveau projet**
4. **Ajouter PostgreSQL** :
   - Cliquer sur "New" → "Database" → "PostgreSQL"
   - Noter les informations de connexion

5. **Déployer le backend** :
   - Cliquer sur "New" → "GitHub Repo"
   - Sélectionner votre repository
   - Railway détectera automatiquement Python/FastAPI

6. **Variables d'environnement** :
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   CORS_ORIGINS=https://votre-frontend-vercel-url.com
   SECRET_KEY=votre-secret-key
   JWT_SECRET_KEY=votre-jwt-secret-key
   ```

#### **4. Mettre à jour les URLs**

1. **Dans Vercel** : Mettre à jour `NEXT_PUBLIC_API_URL` avec l'URL Railway
2. **Dans Railway** : Mettre à jour `CORS_ORIGINS` avec l'URL Vercel

---

## 🐳 **Option 2 : Déploiement Docker (VPS)**

### **Avantages** :
- ✅ Contrôle total
- ✅ Scalable
- ✅ Professionnel
- ✅ Coût fixe

### **Prérequis** :
- Serveur VPS (Ubuntu 20.04+)
- Docker et Docker Compose installés
- Domaine configuré

### **Étapes de déploiement** :

#### **1. Préparer le serveur**

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

#### **2. Cloner et configurer le projet**

```bash
# Cloner le repository
git clone https://github.com/votre-username/najah-ai.git
cd najah-ai

# Rendre le script exécutable
chmod +x deploy-production.sh

# Exécuter le déploiement
./deploy-production.sh
```

#### **3. Configurer Nginx (reverse proxy)**

```bash
# Installer Nginx
sudo apt install nginx -y

# Créer la configuration
sudo nano /etc/nginx/sites-available/najah-ai
```

**Contenu de la configuration Nginx** :
```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/najah-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### **4. Configurer SSL avec Let's Encrypt**

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

---

## 🔧 **Option 3 : Déploiement DigitalOcean App Platform**

### **Avantages** :
- ✅ Interface simple
- ✅ Scaling automatique
- ✅ Monitoring intégré
- ✅ Base de données gérée

### **Étapes** :

1. **Aller sur [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
2. **Créer une nouvelle app**
3. **Connecter GitHub**
4. **Configuration** :
   - **Frontend** : Dossier `frontend`, Framework Next.js
   - **Backend** : Dossier `backend`, Framework Python
   - **Database** : PostgreSQL

---

## 📊 **Comparaison des Options**

| Option | Coût | Complexité | Contrôle | Scalabilité |
|--------|------|------------|----------|-------------|
| Vercel + Railway | Gratuit | Faible | Moyen | Élevée |
| Docker + VPS | $5-20/mois | Moyenne | Élevé | Élevée |
| DigitalOcean | $12-50/mois | Faible | Moyen | Très élevée |

---

## 🚀 **Déploiement Rapide (5 minutes)**

### **Pour commencer immédiatement** :

1. **Frontend sur Vercel** :
   ```bash
   cd frontend
   npm run build
   # Puis déployer sur vercel.com
   ```

2. **Backend sur Railway** :
   ```bash
   # Déployer directement depuis GitHub sur railway.app
   ```

3. **Mettre à jour les URLs** dans les variables d'environnement

---

## 🔍 **Vérification du Déploiement**

### **Tests à effectuer** :

1. **Frontend** : Vérifier que l'interface se charge
2. **Backend** : Tester `/health` et `/docs`
3. **Authentification** : Tester la connexion
4. **Base de données** : Vérifier les données

### **URLs importantes** :
- **Frontend** : `https://votre-app.vercel.app`
- **Backend API** : `https://votre-app.railway.app`
- **Documentation** : `https://votre-app.railway.app/docs`

---

## 🛠️ **Maintenance et Monitoring**

### **Commandes utiles** :

```bash
# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f

# Redémarrer les services
docker-compose -f docker-compose.prod.yml restart

# Mettre à jour l'application
git pull && docker-compose -f docker-compose.prod.yml up -d --build

# Sauvegarder la base de données
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U najah_user najah_ai > backup.sql
```

### **Monitoring recommandé** :
- **Uptime** : UptimeRobot (gratuit)
- **Logs** : Papertrail ou LogDNA
- **Métriques** : New Relic ou DataDog

---

## 🎯 **Recommandation Finale**

**Pour commencer rapidement** : **Vercel + Railway** (gratuit)
**Pour la production** : **Docker + VPS** (contrôle total)

**Budget recommandé** : $5-15/mois pour commencer

---

## 📞 **Support**

En cas de problème :
1. Vérifier les logs des services
2. Contrôler les variables d'environnement
3. Tester la connectivité réseau
4. Consulter la documentation des plateformes

**Najah AI** - Révolutionner l'analytics éducative avec l'IA 🎓✨

