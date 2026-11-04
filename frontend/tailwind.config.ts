import type { Config } from 'tailwindcss'
import colors from 'tailwindcss/colors'

export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      colors: {
        ...colors,
        primary: {
          50: '#fff1ed',
          100: '#ffe4db',
          200: '#ffc5b0',
          300: '#ff9f7d',
          400: '#ff7445',
          500: '#ec6a38', // Deine Hauptfarbe
          600: '#e85117',
          700: '#c13d0c',
          800: '#9c320e',
          900: '#7e2b0f',
        }
      }
    },
  },
  plugins: [],
} satisfies Config