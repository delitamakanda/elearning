import 'babel-polyfill'

import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App.vue'
import store from './store'

import 'vuetify/dist/vuetify.min.css'
import 'vuetify/src/styles/main.sass'

import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

const opts = {
    iconfont: 'md'
}
Vue.use(Vuetify)

Vue.config.productionTip = false

new Vue({
  store,
  vuetify: new Vuetify(opts),
  render: h => h(App)
}).$mount('#app')
