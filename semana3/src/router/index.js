import { createRouter, createWebHistory } from 'vue-router'
import authStore from '../store'

import LoginView from '../views/LoginView.vue'
import GameListView from '../views/GameListView.vue'
import GameForm from '../views/GameForm.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/games',
    name: 'GameList',
    component: GameListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/games/add',
    name: 'GameAdd',
    component: GameForm,
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
  {
    path: '/games/edit/:id',
    name: 'GameEdit',
    component: GameForm,
    props: true,
    meta: { requiresAuth: true, requiresAdmin: true }
  },

  {
    path: '/',
    redirect: '/login'
  },

  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {

  let isLoggedIn = authStore.state.isLoggedIn;

  if (!isLoggedIn) {
    isLoggedIn = await authStore.checkSession();
  }

  const requiresAuth = to.meta.requiresAuth;

  if (requiresAuth) {
    if (isLoggedIn) {
      if (to.meta.requiresAdmin && !authStore.state.isAdmin) {
        next({ name: 'GameList' });
      } else {
        next();
      }
    } else {
      next({ name: 'Login' });
    }
  } 
  
  else {
    if (to.name === 'Login' && isLoggedIn) {
      next({ name: 'GameList' });
    } else {
      next();
    }
  }
})

export default router
