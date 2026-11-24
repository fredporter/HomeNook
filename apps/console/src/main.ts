/**
 * HomeNest Console — Vue 3 entry point
 * 10-foot media + automation control surface
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'

// CSS imports in layer order: PicoCSS base → USX tokens → theme → standard → home-nest
// Tokens resolve to the canonical package in uCore/packages/usx-tokens via the
// `@udos/usx-tokens` alias in vite.config.ts. HomeNook does not vendor a copy.
import '@picocss/pico'
import '@udos/usx-tokens/tokens/tokens-color.css'
import '@udos/usx-tokens/tokens/tokens-components.css'
import '@udos/usx-tokens/tokens/tokens-spacing.css'
import '@udos/usx-tokens/tokens/tokens-touch.css'
import '@udos/usx-tokens/tokens/tokens-typography.css'
import '@udos/usx-tokens/themes/dark.css'
import '@udos/usx-tokens/usx-standard.css'
import '@udos/usx-tokens/home-nest/console-grid.css'
import '@udos/usx-tokens/home-nest/controller-focus.css'
import '@udos/usx-tokens/home-nest/media-player.css'
// Display profile last: it is attribute-scoped and overrides the console grid defaults.
import '@udos/usx-tokens/home-nest/display-profiles.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')