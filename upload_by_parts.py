#!/usr/bin/env python3
"""
Guide pour uploader le projet par parties sur GitHub
"""

def create_part_zips():
    """Crée des ZIP par parties pour GitHub"""
    
    print("📦 CRÉATION DE ZIP PAR PARTIES POUR GITHUB")
    print("="*50)
    
    parts = {
        "part1_frontend": {
            "description": "Frontend Next.js",
            "include": [
                "frontend/src/",
                "frontend/public/", 
                "frontend/package.json",
                "frontend/next.config.js",
                "frontend/tsconfig.json",
                "frontend/tailwind.config.js"
            ],
            "max_size": "~5MB"
        },
        "part2_backend": {
            "description": "Backend FastAPI", 
            "include": [
                "backend/",
                "api/"
            ],
            "max_size": "~15MB"
        },
        "part3_config": {
            "description": "Configuration et déploiement",
            "include": [
                ".gitignore",
                "requirements.txt",
                "railway.toml", 
                "Procfile",
                "docker-compose.yml",
                "nginx.conf",
                "README.md"
            ],
            "max_size": "~1MB"
        },
        "part4_data": {
            "description": "Données exportées",
            "include": [
                "data_export_*.json",
                "summary_*.txt",
                "export_data.py"
            ],
            "max_size": "~5MB"
        }
    }
    
    print("🎯 PLAN D'UPLOAD PAR PARTIES:")
    print()
    
    for part_name, info in parts.items():
        print(f"📦 {part_name}.zip ({info['max_size']})")
        print(f"   📋 {info['description']}")
        print(f"   📁 Contenu:")
        for item in info['include']:
            print(f"      - {item}")
        print()
    
    print("🚀 PROCÉDURE:")
    print("1. Créer chaque ZIP séparément")
    print("2. Uploader un par un sur GitHub")
    print("3. GitHub reconstituera le projet complet")
    print()
    print("⚠️ IMPORTANT: Commencez par part2_backend (le plus important)")

if __name__ == "__main__":
    create_part_zips()

