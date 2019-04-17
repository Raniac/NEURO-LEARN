import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: resolve => require(['@/pages/home/home'], resolve)
    },
    {
      path: '/overview',
      component: resolve => require(['@/pages/overview/overview'], resolve)
    },
    {
      path: '/newdl',
      component: resolve => require(['@/pages/newtask/newdl'], resolve)
    },
    {
      path: '/newml',
      component: resolve => require(['@/pages/newtask/newml'], resolve)
    },
    {
      path: '/newsa',
      component: resolve => require(['@/pages/newtask/newsa'], resolve)
    },
    {
      path: '/submissions',
      component: resolve => require(['@/pages/submissions/submissions'], resolve)
    },
    {
      path: '/viewer',
      component: resolve => require(['@/pages/viewer/viewer'], resolve)
    },
    {
      path: '/help',
      component: resolve => require(['@/pages/help/help'], resolve)
    },
    {
      path: '/test',
      component: resolve => require(['@/pages/test/test'], resolve)
    }
  ]
})
