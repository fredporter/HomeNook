import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// Code root holds the sibling repositories. USX tokens have one home:
// uCore/packages/usx-tokens. HomeNook consumes them through this alias and
// never vendors a copy (see docs/architecture.md).
const CODE_ROOT = resolve(__dirname, '../../..')

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@udos/usx-tokens': resolve(CODE_ROOT, 'uCore/packages/usx-tokens'),
    },
  },
  server: {
    port: 5184,
    proxy: {
      '/api': 'http://127.0.0.1:8174',
    },
  },
})