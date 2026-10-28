/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {
    colors: {
      ink: "#202b2b", muted: "#788482", canvas: "#f6f7f4", panel: "#ffffff", line: "#e8ece8",
      teal: { 50: "#eaf5f1", 100: "#d5ebe3", 500: "#428b78", 600: "#327562", 700: "#245e4e" },
      amber: { 50: "#fbf3e5", 100: "#f6e7c7", 600: "#a96d22" },
      rose: { 50: "#faecea", 100: "#f4d9d5", 600: "#b6544b" }
    },
    fontFamily: { sans: ["DM Sans", "sans-serif"], display: ["Manrope", "sans-serif"] },
    boxShadow: { soft: "0 8px 28px rgba(28, 43, 39, 0.035)" }
  }},
  plugins: []
};