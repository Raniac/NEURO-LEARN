// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import '../theme/index.css'
import axios from 'axios'

Vue.prototype.$axios = axios
axios.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken')

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.use(ElementUI, { locale })

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

function getCookie (name) {
  var arr
  var reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
  if (arr === document.cookie.match(reg)) {
    return unescape(arr[2])
  } else {
    return null
  }
}

function setCookie (name, value, days) {
  var exp = new Date()
  exp.setTime(exp.getTime() + days * 24 * 60 * 60 * 1000)
  document.cookie = name + '=' + escape(value) + ';expires=' + exp.toGMTString()
}

export {
  getCookie,
  setCookie
}
