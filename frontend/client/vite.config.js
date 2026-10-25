import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/static/",
  resolve: {
    dedupe: ["react", "react-dom", "react-router", "react-router-dom"],
  },
  server: {
    fs: {
      allow: ["../.."],
    },
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/about": "http://127.0.0.1:8000",
      "/contact": "http://127.0.0.1:8000",
    },
  },
});
