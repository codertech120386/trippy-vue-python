import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import NavBar from './components/NavBar'
import {TokenService} from './utils/token.service'
import store from './store'
import {AuthAPIService} from './utils/api.service'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        allowedRoles: ['admin', 'user', 'user_manager']
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "about" */ './views/Login.vue'),
      meta: {
        public: true,
        onlyWhenLoggedOut: true,
        allowedRoles: ['admin', 'user', 'user_manager']
      }
    },
    {
      path: '/register',
      name: 'register',
      meta: {
        public: true,
        onlyWhenLoggedOut: true,
        allowedRoles: ['admin', 'user', 'user_manager']
      },
      component: () => import(/* webpackChunkName: "about" */ './views/Register.vue')
    },
    {
      path: '/users',
      name: 'users',
      meta:{
        allowedRoles: ['admin', 'user_manager']
      },
      components: {
        default:() => import(/* webpackChunkName: "about" */ './views/Users.vue'),
        a: NavBar
      }
    },
    {
      path: '/trips',
      name: 'trips',
      meta:{
        allowedRoles: ['admin', 'user']
      },
      components: {
        default:() => import(/* webpackChunkName: "about" */ './views/Trips.vue'),
        a: NavBar
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isPublic = to.matched.some(record => record.meta.public)
  const onlyWhenLoggedOut = to.matched.some(record => record.meta.onlyWhenLoggedOut)
  const allowedRoles = to.meta.allowedRoles
  const loggedIn = !!TokenService.getToken();


  if (!isPublic && !loggedIn) {
    return next({
      path:'/login'
    });
  }

  if (isPublic && !loggedIn) {
    return next();
  }

  if(!store.state.role){
    AuthAPIService.get('/users/verify',{}).then(resp => {
      store.commit('set_role', resp.data.data.role)

      if (loggedIn && onlyWhenLoggedOut) {
        return next('/')
      }
      if (allowedRoles.indexOf(store.state.role) < 0){
        return next('/')
      }

      next();

    }).catch(() => {
      // logout the user
      TokenService.removeToken()
      return next({
        path:'/login'
      });
    })
  } else {
  
    if (loggedIn && onlyWhenLoggedOut) {
      return next('/')
    }
    if (allowedRoles.indexOf(store.state.role) < 0){
      return next('/')
    }
    next();
  }
})

export default router
