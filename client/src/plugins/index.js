/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import {setupVuetify} from './vuetify'
import router from '@/router'

export function registerPlugins (app) {
  app
    .use(setupVuetify())
    .use(router)
}
