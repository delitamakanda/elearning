import Vue from 'vue'
import Vuex from 'vuex'

import * as event from './state/event'

Vue.use(Vuex)

const store = new Vuex.Store({
  strict: true,
  modules: {
      event
  }
})

export default store
