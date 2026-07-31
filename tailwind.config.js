/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",

    "./events/templates/**/*.html",
    "./accounts/templates/**/*.html",

    "./events/**/*.py",
    "./accounts/**/*.py",
    "./config/**/*.py",
  ],

  theme: {
    extend: {
      fontFamily: {
        heading: ["Cormorant Garamond", "serif"],
        body: ["Inter", "sans-serif"],
      },

      boxShadow: {
        card: "0 10px 30px rgba(15,23,42,.08)",
      },

      borderRadius: {
        xl2: "20px",
      },

      colors: {
        primary: "#111827",
        secondary: "#64748B",
        background: "#F8FAFC",
      },
    },
  },

  plugins: [],
}