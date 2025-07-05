
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: { extend: {} },
  plugins: []
}

// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Aquí defines tu nueva fuente. 'sans' es el valor por defecto para fuentes sin serifa.
        // Puedes darle un nombre personalizado si quieres, por ejemplo 'inter'.
        sans: ['Inter', 'sans-serif'], // Reemplaza 'Inter' con el nombre de tu fuente
        // Si quieres otra fuente para títulos, podrías añadir:
        // display: ['Montserrat', 'sans-serif'],
      }
    },
  },
  plugins: [],
}