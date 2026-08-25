module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      colors: {
        pomegranate: { DEFAULT: '#fb4d1c', light: '#fc8260', dark: '#c83d16', darker: '#641e0b', lightest: '#feede8', lighter: '#fedbd1' },
        jaffa: { DEFAULT: '#f28c34', dark: '#c17029', light: '#f5ae70', lightest: '#fdf3ea', lighter: '#fce8d6' },
        ink: { DEFAULT: '#191919', soft: '#4c4c4c', muted: '#7f7f7f', line: '#e5e5e5', bg: '#f2f2f2' }
      },
      fontFamily: {
        display: ['"Yanone Kaffeesatz"', 'Impact', 'sans-serif'],
        body: ['"Hind"', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
};
