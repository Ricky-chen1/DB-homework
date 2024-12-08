import Home from '@/views/Home.vue'
import BookList from '@/views/BookList.vue'
import BookDetail from '@/views/BookDetail.vue'
import UserProfile from '@/views/UserProfile.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Regitser.vue'
import BookPublish from '@/views/BookPublish.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/bookList',
      name: 'bookList',
      component: BookList
    },
    {
      path: '/book/:id',
      name: 'bookDetail',
      component: BookDetail,
      props: true // Pass route params as props to the component
    },
    {
      path: '/user',
      name: 'userProfile',
      component: UserProfile
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/publish',
      name: 'bookPublish',
      component: BookPublish
    }
  ],
})

export default router
