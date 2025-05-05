/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export function setupVuetify(){
  return createVuetify({
    //
    icons: {
      defaultSet: "mdi",
    },
    theme: {
      themes: {
        light: {
          colors: {
            primary: "#393939",
            blank: "#FFFFFF",
            "primary-lighten": "#D2D3D5",
            "primary-colored": "#42A3CE",
          },
        },
      },
    },
  })
}
