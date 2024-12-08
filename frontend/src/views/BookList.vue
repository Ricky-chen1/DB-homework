<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// 用户登录状态和书籍数据
const isLoggedIn = ref(false); // 模拟用户登录状态
const books = ref([]);
const loading = ref(true);
const router = useRouter();

// 模拟获取登录信息
const fetchUserStatus = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/user/status`);
    isLoggedIn.value = response.data.isLoggedIn;
  } catch (error) {
    console.error('无法获取用户登录状态:', error);
    isLoggedIn.value = false;
  }
};

// 获取书籍数据
const fetchBooks = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/book/list`);
    books.value = response.data.books || [];
  } catch (error) {
    console.error('无法获取书籍数据:', error);
  } finally {
    loading.value = false;
  }
};

// 页面加载时获取数据
onMounted(() => {
  const user = localStorage.getItem('user');  // 从 localStorage 获取登录状态
  if (user) {
    isLoggedIn.value = true;  // 如果有用户信息，设置为已登录
  } else {
    isLoggedIn.value = false;  // 未登录
    router.push('/login');  // 重定向到登录页面
  }

  fetchUserStatus();
  fetchBooks();
});

// 点击查看书籍详情
const viewBookDetail = (bookId: string) => {
  // 跳转到书籍详情页
  console.log('查看书籍详情', bookId);
};
</script>

<template>
  <div class="book-list">
    <div class="container">
      <h1 class="page-title">Book List</h1>

      <!-- 登录提示 -->
      <div v-if="!isLoggedIn" class="login-prompt">
        <p>Please log in to view the full book list.</p>
      </div>

      <!-- 书籍列表 -->
      <div v-if="isLoggedIn && !loading" class="book-grid">
        <div v-for="book in books" :key="book.id" class="book-card">
          <img 
            v-if="book.image" 
            :src="book.image" 
            alt="Book Cover" 
            class="book-cover" 
          />
          <h2 class="book-title">{{ book.title }}</h2>
          <p class="book-author">Author: {{ book.author }}</p>
          <p class="book-price">Price: ${{ book.price }}</p>
          <button 
            @click="viewBookDetail(book.id)" 
            class="view-details-button">
            查看书籍详情
          </button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else-if="loading" class="loading-message">
        Loading books... Please wait.
      </div>

      <!-- 无书籍提示 -->
      <div v-else class="loading-message">
        暂无可购买书籍，请等待他人发布
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-list {
  padding: 20px;
  background-color: #f4f4f9;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  width: 100%;
}

.book-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.book-cover {
  width: 100px;
  height: auto;
  border-radius: 5px;
  margin-bottom: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.book-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #444;
}

.book-author,
.book-price {
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.view-details-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.9rem;
}

.view-details-button:hover {
  background-color: #0056b3;
}

.loading-message {
  font-size: 1rem;
  color: #555;
  text-align: center;
}

.login-prompt {
  font-size: 1.2rem;
  color: #d9534f;
  text-align: center;
  margin-top: 30px;
}
</style>
