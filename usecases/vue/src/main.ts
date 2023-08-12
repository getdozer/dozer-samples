import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)

// Vuetify
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'

const vuetify = createVuetify({
  components,
  directives,
})

app.use(vuetify)

// Google Map
// import VueGoogleMaps from '@fawmi/vue-google-maps'
import VueGoogleMaps from 'vue-google-maps-community-fork'
app.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAV1g7kB_iY7H3BNjgtbc7Aaa8q1_isDJA',
  },
})

app.mount('#app')
