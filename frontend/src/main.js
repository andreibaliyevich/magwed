import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import vuetify from './vuetify'

import uiComponents from './components/UI'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(createHead())
app.use(vuetify)

uiComponents.forEach(component => {
  app.component(component.name, component)
})

app.mount('#app')
