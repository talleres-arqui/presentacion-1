import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 8080, // 👈 el puerto donde corre tu app Vue
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 👈 backend FastAPI
        changeOrigin: true,               // permite redirección entre dominios
        rewrite: (path) => path.replace(/^\/api/, ''), // elimina el prefijo /api
      },
    },
  },
});
