import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "../styles/index.css"; // Import des nouveaux styles améliorés
import { ThemeProvider } from "../contexts/ThemeContext";
import { AccessibilityProvider } from "../components/AccessibilityProvider";
import { AuthProvider } from "../contexts/AuthContext";
import { DashboardProvider } from "../contexts/DashboardContext";
import ThemeToggle from "../components/ThemeToggle";
import NotificationSystem from "../components/NotificationSystem";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Najah AI - Plateforme Éducative Intelligente",
  description: "Plateforme éducative moderne avec IA avancée, gamification et analytics en temps réel",
  keywords: "éducation, IA, apprentissage, gamification, analytics, quiz, étudiants, professeurs",
  authors: [{ name: "Najah AI Team" }],
  creator: "Najah AI",
  publisher: "Najah AI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://najah-ai.com"),
  alternates: {
    canonical: "/",
    languages: {
      "fr-FR": "/fr",
      "en-US": "/en",
    },
  },
  openGraph: {
    title: "Najah AI - Plateforme Éducative Intelligente",
    description: "Plateforme éducative moderne avec IA avancée, gamification et analytics en temps réel",
    url: "https://najah-ai.com",
    siteName: "Najah AI",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Najah AI - Plateforme Éducative",
      },
    ],
    locale: "fr_FR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Najah AI - Plateforme Éducative Intelligente",
    description: "Plateforme éducative moderne avec IA avancée, gamification et analytics en temps réel",
    images: ["/twitter-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "your-google-verification-code",
    yandex: "your-yandex-verification-code",
    yahoo: "your-yahoo-verification-code",
  },
  category: "education",
  classification: "educational software",
  referrer: "origin-when-cross-origin",
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#3b82f6" },
    { media: "(prefers-color-scheme: dark)", color: "#1e40af" },
  ],
  viewport: {
    width: "device-width",
    initialScale: 1,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <meta name="theme-color" content="#3b82f6" />
        <meta name="color-scheme" content="light dark" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <ThemeProvider>
          <AccessibilityProvider>
            <AuthProvider>
              <DashboardProvider>
                <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
                  {/* Header global avec notifications et thème */}
                  <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                      <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-4">
                          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                            Najah AI
                          </h1>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                          <ThemeToggle />
                          <NotificationSystem />
                        </div>
                      </div>
                    </div>
                  </header>

                  {/* Contenu principal */}
                  <main className="flex-1 pb-32">
                    {children}
                  </main>
                </div>
              </DashboardProvider>
            </AuthProvider>
          </AccessibilityProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
