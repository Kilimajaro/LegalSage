//
import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login/index.vue'
import Header from '@/views/Header/index.vue'
import Ask from '@/views/Ask/index.vue'
import Describe from '@/views/Describe/index.vue'
import Document from '@/views/Document/index.vue'
import Request from '@/views/Request/index.vue'

// 创建路由实力
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Header,
    },
    {
      path: '/login',
      component: Login,
    },
    {
      path: '/ask',
      component: Ask,
      children: [
        {
          path: 'describe',
          component: Describe,
          name: 'describe',
        },
        {
          path: 'document',
          component: Document,
          name: 'document',
        },
        {
          path: '',
          component: Request,
          name: 'request',
        },
      ],
    },
  ],
})

export default router
