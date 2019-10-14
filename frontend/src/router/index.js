import Vue from 'vue'
import Router from 'vue-router'

import home from '@/pages/home'
import login from '@/pages/login'
import profile from '@/pages/profile'
import projectsOverview from '@/pages/projects/overview'
import projectsData from '@/pages/projects/data'
import projectsNewProjBeta from '@/pages/projects/newproj/beta'
import analysisOverview from '@/pages/analysis/overview'
import analysisNewtaskNewDL from '@/pages/analysis/newtask/newdl'
import analysisNewtaskNewML from '@/pages/analysis/newtask/newml'
import analysisNewtaskNewSA from '@/pages/analysis/newtask/newsa'
import analysisSubmissions from '@/pages/analysis/submissions'
import analysisViewer from '@/pages/analysis/viewer'
import about from '@/pages/about'
import test from '@/pages/test'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      component: login
    },
    {
      path: '/login',
      component: login
    },
    {
      path: '/home',
      component: home
    },
    {
      path: '/profile',
      component: profile
    },
    {
      path: '/projects/overview',
      component: projectsOverview
    },
    {
      path: '/projects/data',
      component: projectsData
    },
    {
      path: '/projects/newproj/beta',
      component: projectsNewProjBeta
    },
    {
      path: '/analysis/overview',
      component: analysisOverview
    },
    {
      path: '/analysis/newtask/newdl',
      component: analysisNewtaskNewDL
    },
    {
      path: '/analysis/newtask/newml',
      component: analysisNewtaskNewML
    },
    {
      path: '/analysis/newtask/newsa',
      component: analysisNewtaskNewSA
    },
    {
      path: '/analysis/submissions',
      component: analysisSubmissions
    },
    {
      path: '/analysis/viewer',
      component: analysisViewer
    },
    {
      path: '/about',
      component: about
    },
    {
      path: '/test',
      component: test
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login' || to.path === '/') {
    next()
  } else {
    let token = sessionStorage.getItem('Authorization')

    if (token === 'null' || token === '' || token === null) {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
