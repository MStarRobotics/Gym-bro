/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00D4FF',
          glow: '#00D4FF',
        },
        secondary: {
          DEFAULT: '#00FF88',
          glow: '#00FF88',
        },
        accent: {
          DEFAULT: '#FF0080',
          glow: '#FF0080',
        },
        background: {
          dark: '#0A0A0F',
          surface: '#1A1A2E',
          card: '#16213E',
        },
      },
    },
  },
  plugins: [],
};
