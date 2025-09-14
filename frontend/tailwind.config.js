/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(40px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in-left': {
          '0%': { opacity: '0', transform: 'translateX(-40px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'fade-in-right': {
          '0%': { opacity: '0', transform: 'translateX(40px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'pulse-slow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '.5' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.8s cubic-bezier(0.4,0,0.2,1) both',
        'fade-in-up': 'fade-in-up 0.8s cubic-bezier(0.4,0,0.2,1) both',
        'fade-in-left': 'fade-in-left 0.8s cubic-bezier(0.4,0,0.2,1) both',
        'fade-in-right': 'fade-in-right 0.8s cubic-bezier(0.4,0,0.2,1) both',
        'pulse-slow': 'pulse-slow 2s infinite',
      },
    },
  },
  plugins: [],
}; 