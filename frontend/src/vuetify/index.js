import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import colors from 'vuetify/util/colors'

export default createVuetify({
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          primary: colors.red.darken1,
          secondary: colors.grey.darken1,
          success: colors.green.base,
          info: colors.blue.base,
          warning: colors.orange.darken1,
          error: colors.red.darken4
        }
      }
    }
  }
})
