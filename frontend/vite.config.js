import { defineConfig } from 'vite'

// Serving the standalone Bio-Synthesis HUD (no React build needed)
export default defineConfig({
  server: {
    port: 5173,
    open: true,
  },
})
