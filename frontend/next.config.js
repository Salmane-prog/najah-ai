/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  headers: async () => {
    return [
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate',
          },
        ],
      },
    ];
  },
  // Ajouter une configuration pour gérer les erreurs de connexion
  async redirects() {
    return [
      {
        source: '/api/health',
        destination: 'http://localhost:8000/health',
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig; 