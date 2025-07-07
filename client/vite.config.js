import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: '../static/build',
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      input: 'src/main.js'
    }
  },
}); 