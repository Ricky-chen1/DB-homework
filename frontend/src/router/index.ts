import Home from '@/views/Home.vue';
import BookList from '@/views/BookList.vue';
import BookDetail from '@/views/BookDetail.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Regitser.vue';
import BookPublish from '@/views/BookPublish.vue';
import Bookshelf from '@/views/Bookshelf.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home',  // 默认跳转到 /home 路由
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
    },
    {
      path: '/bookList',
      name: 'bookList',
      component: BookList,
    },
    {
      path: '/book/:id',
      name: 'bookDetail',
      component: BookDetail,
      props: true,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/bookshelf',
      name: 'bookshelf',
      component: Bookshelf,
    },
    {
      path:'/publish',
      name:'publish',
      component: BookPublish,
    },
  ],
});

export default router;
