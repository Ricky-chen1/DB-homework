<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import request from '@/utils/request'; // 使用封装的 Axios 实例
import type { Book } from '@/pack/book';

const book = ref<Book>(null);
const route = useRoute();
const router = useRouter();

// 获取书籍详情
const fetchBookDetail = async () => {
  try {
    const response = await request.get(`/api/book/${route.params.id}`,{
    });
    book.value = response.data || null;
  } catch (error) {
    console.error('获取书籍详情失败:', error);
  }
};

// 跳转至创建订单页面
const goToOrderCreate = () => {
  if (book.value) {
    // 传递书籍信息和卖家信息
    router.push({
    path: '/orderCreate',
    query: {
      bookId: book.value.id,
      bookTitle: book.value.title, // 书名
      bookPrice: book.value.price, // 传递书的定价
      publisherId: book.value.publisher_id, // 改为 publisherId
      },
    });
  }
};

onMounted(() => {
  fetchBookDetail();
});
</script>

<template>
  <div class="book-detail">
    <div class="container">
      <div v-if="book" class="book-card">
        <!-- 书籍封面 -->
        <img 
          :src="book.cover_url" 
          alt="Book Cover" 
          class="book-cover" 
        />

        <!-- 书籍信息 -->
        <div class="book-info">
          <h1 class="book-title">{{ book.title }}</h1>
          <p class="book-author"><strong>作者:</strong> {{ book.author }}</p>
          <p class="book-price"><strong>价格:</strong> ¥{{ book.price }}</p>
          <p class="book-description"><strong>描述:</strong> {{ book.description || '暂无描述信息' }}</p>
          <p class="book-created"><strong>发布时间:</strong> {{ new Date(book.created_at).toLocaleString() }}</p>
        </div>

        <!-- 购买按钮 -->
        <button 
          class="buy-button" 
          @click="goToOrderCreate"
        >
          立即购买
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-else class="loading-message">
        正在加载书籍详情，请稍候...
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-detail {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #eef2f3, #ffffff);
  padding: 30px;
}

.container {
  max-width: 800px;
  width: 100%;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 25px;
  position: relative;
}

.book-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.book-cover {
  width: 220px;
  height: auto;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.book-info {
  font-family: 'Roboto', sans-serif;
  line-height: 1.6;
}

.book-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.book-author,
.book-price,
.book-description,
.book-created {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #555;
}

.book-description {
  margin-top: 10px;
  font-style: italic;
}

.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.buy-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #ff5722;
  color: white;
  padding: 12px 25px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
}

.buy-button:hover {
  background: #e64a19;
  box-shadow: 0 6px 15px rgba(255, 87, 34, 0.4);
  transform: scale(1.05);
}
</style>