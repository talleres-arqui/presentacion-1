import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 8081,
    host: true,
    proxy: {
      '/api': {
        target: 'http://host.docker.internal:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/ws': {
        target: 'ws://host.docker.internal:8001',
        ws: true,              // <--- MUY IMPORTANTE
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
