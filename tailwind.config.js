/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./events/templates/**/*.html",
    "./accounts/templates/**/*.html",
    "./events/views/**/*.py",
    "./accounts/**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}