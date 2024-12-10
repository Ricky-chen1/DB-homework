<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const publishedBooks = ref<any[]>([]); // 已发布书籍
const soldBooks = ref<any[]>([]); // 已售出书籍
const errorMessage = ref('');

// 获取用户已发布书籍
const fetchPublishedBooks = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      errorMessage.value = '用户未登录，请重新登录。';
      router.push('/login');
      return;
    }

    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/book/published`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    publishedBooks.value = response.data.books || [];
  } catch (error) {
    console.error('Failed to fetch published books:', error);
    errorMessage.value = '获取已发布书籍失败，请稍后再试。';
  }
};

// 获取用户已售出书籍
const fetchSoldBooks = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      errorMessage.value = '用户未登录，请重新登录。';
      return;
    }

    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/book/sold`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    soldBooks.value = response.data.books || [];
  } catch (error) {
    console.error('Failed to fetch sold books:', error);
    errorMessage.value = '获取已售出书籍失败，请稍后再试。';
  }
};

// 页面加载时获取数据
onMounted(() => {
  fetchPublishedBooks();
  fetchSoldBooks();
});

// 跳转到发布书籍页面
const goToPublishPage = () => {
  router.push('/publish');
};
</script>

<template>
  <div class="bookshelf-container">
    <header class="header">
      <h1>我的书架</h1>
      <button class="publish-button" @click="goToPublishPage">
        <i class="iconfont icon-plus"></i>
      </button>
    </header>

    <div class="books-list-container">
      <section class="books-section">
        <h2>已发布书籍</h2>
        <ul>
          <li v-for="book in publishedBooks" :key="book.id" class="book-item">
            <h3>{{ book.title }}</h3>
            <p>作者: {{ book.author }}</p>
            <p>售价: ￥{{ book.price }}</p>
          </li>
        </ul>
      </section>

      <section class="books-section">
        <h2>已售出书籍</h2>
        <ul>
          <li v-for="book in soldBooks" :key="book.id" class="book-item">
            <h3>{{ book.title }}</h3>
            <p>作者: {{ book.author }}</p>
            <p>售价: ￥{{ book.price }}</p>
          </li>
        </ul>
      </section>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
.bookshelf-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.publish-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #4caf50;
}

.publish-button:hover {
  color: #388e3c;
}

.books-list-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.books-section {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.books-section h2 {
  margin-top: 0;
}

.book-item {
  margin-bottom: 15px;
}

.error {
  color: red;
  text-align: center;
}
</style>

<!-- 引用 iconfont 的外部样式 -->
<link rel="stylesheet" href="https://at.alicdn.com/t/c/font_4756601_9mxxkv4q5qo.css">
