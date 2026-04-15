/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        boardBg: '#1e293b',
        cardBg: '#334155',
        columnBg: '#0f172a',
      }
    },
  },
  plugins: [],
}
