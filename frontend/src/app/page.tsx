"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth  } from '../hooks/useAuth';
import { Card } from "../components/Card";
import Button from "../components/Button";
import Logo from "../components/Logo";
import {
  BookOpen,
  Heart,
  Shield,
  ArrowRight,
  Target,
  TrendingUp,
  Award,
  GraduationCap,
} from "lucide-react";

export default function HomePage() {
  const { isAuthenticated, user, isLoading } = useAuth();
  const router = useRouter();
  const [shouldRedirect, setShouldRedirect] = useState(false);

  useEffect(() => {
    // Attendre que l'authentification soit chargée
    if (!isLoading) {
      // Vérifier si l'utilisateur est authentifié ET a un token valide
      const token = localStorage.getItem("najah_token");
      const userData = localStorage.getItem("najah_user");
      
      if (isAuthenticated && user && token && userData) {
        // Vérifier si le token n'est pas expiré
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          const now = new Date();
          const exp = new Date(payload.exp * 1000);
          
          if (exp > now) {
            setShouldRedirect(true);
            router.push(`/dashboard/${user.role}`);
          } else {
            // Token expiré, nettoyer le localStorage
            localStorage.removeItem("najah_token");
            localStorage.removeItem("najah_user");
            console.log("Token expiré, redirection annulée");
          }
        } catch (error) {
          // Token invalide, nettoyer le localStorage
          localStorage.removeItem("najah_token");
          localStorage.removeItem("najah_user");
          console.log("Token invalide, redirection annulée");
        }
      }
    }
  }, [isAuthenticated, user, isLoading, router]);

  // Afficher un loader pendant la vérification de l'authentification
  if (isLoading || shouldRedirect) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  const features = [
    {
      icon: <BookOpen className="text-blue-600" size={32} />,
      title: "Apprentissage Personnalisé",
      description: "Des parcours adaptés à votre niveau et votre style d&apos;apprentissage",
    },
    {
      icon: <Target className="text-green-600" size={32} />,
      title: "QCM Intelligents",
      description: "Génération automatique de quiz avec 20% IA et 80% base de données",
    },
    {
      icon: <TrendingUp className="text-purple-600" size={32} />,
      title: "Suivi de Progression",
      description: "Analytics détaillés et recommandations personnalisées",
    },
    {
      icon: <Award className="text-yellow-600" size={32} />,
      title: "Gamification",
      description: "Système de badges, points et récompenses pour motiver l&apos;apprentissage",
    },
  ];

  const interfaces = [
    {
      role: "student",
      title: "Interface Élève",
      description: "Profil personnalisé, historique d&apos;apprentissage, tableau de bord adapté à l&apos;âge",
      icon: <BookOpen className="text-blue-600" size={24} />,
      color: "from-blue-50 to-blue-100 border-blue-200",
    },
    {
      role: "teacher",
      title: "Interface Enseignant",
      description: "Gestion de classes, tableaux de bord analytiques, création de parcours",
      icon: <GraduationCap className="text-green-600" size={24} />,
      color: "from-green-50 to-green-100 border-green-200",
    },
    {
      role: "parent",
      title: "Interface Parent",
      description: "Suivi de progression des enfants, communication avec enseignants",
      icon: <Heart className="text-purple-600" size={24} />,
      color: "from-purple-50 to-purple-100 border-purple-200",
    },
    {
      role: "admin",
      title: "Interface Administrateur",
      description: "Gestion des utilisateurs, configuration plateforme, contenus pédagogiques",
      icon: <Shield className="text-red-600" size={24} />,
      color: "from-red-50 to-red-100 border-red-200",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center gap-3">
              <Logo size={40} />
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Najah AI</h1>
                <p className="text-sm text-gray-600">Plateforme d&apos;Apprentissage Adaptatif</p>
              </div>
            </div>
            <Button
              variant="primary"
              onClick={() => router.push("/login")}
              icon={<ArrowRight size={16} />}
            >
              Se connecter
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold text-gray-800 mb-6 animate-fade-in-up">
            Plateforme <span className="text-blue-600">Éducative</span> <span className="text-purple-600">Innovante</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto animate-fade-in-up">
            Découvrez une plateforme d&apos;enseignement adaptatif qui s&apos;adapte à chaque apprenant grâce à l&apos;intelligence artificielle et des parcours personnalisés.
          </p>
          <div className="flex gap-4 justify-center animate-fade-in-up">
            <Button
              variant="primary"
              size="lg"
              onClick={() => router.push("/login")}
              icon={<ArrowRight size={20} />}
            >
              Commencer maintenant
            </Button>
            <Button
              variant="secondary"
              size="lg"
              onClick={() =>
                document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })
              }
            >
              En savoir plus
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4 animate-fade-in-up">
              Fonctionnalités Principales
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto animate-fade-in-up">
              Une plateforme complète pour tous les acteurs de l&apos;éducation
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card
                key={index}
                variant="gradient"
                className="text-center p-6 animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1 + 0.2}s` }}
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Interfaces Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4 animate-fade-in-up">
              Interfaces Spécialisées
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto animate-fade-in-up">
              Chaque utilisateur bénéficie d&apos;une interface adaptée à ses besoins
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {interfaces.map((interface_, index) => (
              <Card
                key={index}
                variant="gradient"
                className={`bg-gradient-to-br ${interface_.color} p-6 hover:shadow-lg transition-all duration-300 cursor-pointer animate-fade-in-up`}
                style={{ animationDelay: `${index * 0.1 + 0.2}s` }}
                onClick={() => router.push("/login")}
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">{interface_.icon}</div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">{interface_.title}</h3>
                    <p className="text-gray-600 mb-4">{interface_.description}</p>
                    <Button
                      variant="secondary"
                      size="sm"
                      icon={<ArrowRight size={14} />}
                    >
                      Tester l&apos;interface
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">1000+</div>
              <div className="text-gray-600">Élèves actifs</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">50+</div>
              <div className="text-gray-600">Enseignants</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">200+</div>
              <div className="text-gray-600">QCM générés</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-yellow-600 mb-2">95%</div>
              <div className="text-gray-600">Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4 animate-fade-in-up">
            Prêt à transformer l&apos;apprentissage ?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto animate-fade-in-up">
            Rejoignez notre plateforme et découvrez une nouvelle façon d&apos;apprendre et d&apos;enseigner.
          </p>
          <Button
            variant="secondary"
            size="lg"
            onClick={() => router.push("/login")}
            icon={<ArrowRight size={20} />}
            className="bg-white text-blue-600 hover:bg-gray-100"
          >
            Commencer gratuitement
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <Logo size={32} />
                <span className="text-xl font-bold">Najah AI</span>
              </div>
              <p className="text-gray-400">
                Plateforme d&apos;apprentissage adaptatif pour l&apos;éducation du futur.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Interfaces</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Élèves</li>
                <li>Enseignants</li>
                <li>Parents</li>
                <li>Administrateurs</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Fonctionnalités</h3>
              <ul className="space-y-2 text-gray-400">
                <li>QCM Intelligents</li>
                <li>Analytics</li>
                <li>Gamification</li>
                <li>Communication</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Documentation</li>
                <li>Contact</li>
                <li>FAQ</li>
                <li>Mentions légales</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Najah AI. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}