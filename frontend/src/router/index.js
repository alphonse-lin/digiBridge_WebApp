import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Layout,
    children: [
      {
        path: 'bridge-monitor',
        name: 'bridge-monitor',
        component: () => import('../views/bridge-monitor/index.vue')
      }
      // {
      //   path: 'others',
      //   name: 'others',
      //   redirect: '/others/suncalc',
      //   children: [
      //     {
      //       path: 'suncalc',
      //       name: 'suncalc',
      //       component: () => import('../views/others/suncalc/index.vue')
      //     }
      //   ]
      // }
    ]
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
