import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: resolve => require(['@/pages/home'], resolve)
    },
    {
      path: '/profile',
      component: resolve => require(['@/pages/profile'], resolve)
    },
    {
      path: '/projects/overview',
      component: resolve => require(['@/pages/projects/overview'], resolve)
    },
    {
      path: '/projects/data/ad_with_smri',
      component: resolve => require(['@/pages/projects/data/ad_with_smri'], resolve)
    },
    {
      path: '/projects/data/sz_with_fmri',
      component: resolve => require(['@/pages/projects/data/sz_with_fmri'], resolve)
    },
    {
      path: '/projects/data/sz_with_sfmri',
      component: resolve => require(['@/pages/projects/data/sz_with_sfmri'], resolve)
    },
    {
      path: '/analysis/overview',
      component: resolve => require(['@/pages/analysis/overview'], resolve)
    },
    {
      path: '/analysis/newtask/newdl',
      component: resolve => require(['@/pages/analysis/newtask/newdl'], resolve)
    },
    {
      path: '/analysis/newtask/newml',
      component: resolve => require(['@/pages/analysis/newtask/newml'], resolve)
    },
    {
      path: '/analysis/newtask/newsa',
      component: resolve => require(['@/pages/analysis/newtask/newsa'], resolve)
    },
    {
      path: '/analysis/submissions',
      component: resolve => require(['@/pages/analysis/submissions'], resolve)
    },
    {
      path: '/analysis/viewer',
      component: resolve => require(['@/pages/analysis/viewer'], resolve)
    },
    {
      path: '/help',
      component: resolve => require(['@/pages/help'], resolve)
    },
    {
      path: '/test',
      component: resolve => require(['@/pages/test'], resolve)
    }
  ]
})
