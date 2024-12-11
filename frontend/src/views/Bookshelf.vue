<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import type { Book, GetBookListResponse } from '@/pack/book';
import request from '@/utils/request'; // 使用之前创建的请求工具

const router = useRouter();

const publishedBooks = ref<Book[]>([]); // 已发布书籍
const soldBooks = ref<Book[]>([]); // 已售出书籍
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

    const response = await request.get<GetBookListResponse>('/api/book/published', {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      publishedBooks.value = response.data || [];
      console.log(publishedBooks);
    } else {
      errorMessage.value = response.msg;
    }
  } catch (error) {
    console.error('获取已发布书籍失败:', error);
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

    const response = await request.get<GetBookListResponse>('/api/book/sold', {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      soldBooks.value = response.data || [];
    } else {
      errorMessage.value = response.msg;
    }
  } catch (error) {
    console.error('获取已售出书籍失败:', error);
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
      <button class="publish-button" @click="goToPublishPage" title="发布书籍">
        <img src="@/assets/plus.svg" alt="Publish" class="publish-icon" />
        <span class="publish-text">发布书籍</span>
      </button>
    </header>

    <div class="books-list-container">
      <!-- 已发布书籍 -->
      <section class="books-section">
        <h2>已发布书籍</h2>
        <ul>
          <li v-for="book in publishedBooks" :key="book.id" class="book-item">
            <div class="book-cover">
              <img
                :src="book.cover_url || '@/assets/bg_image02.png'"
                alt="Book Cover"
                class="book-cover-img"
              />
            </div>
            <div class="book-info">
              <h3>{{ book.title }}</h3>
              <p>作者: {{ book.author }}</p>
              <p>售价: ￥{{ book.price }}</p>
              <div v-if="book.categories && book.categories.length" class="book-categories">
                <span v-for="category in book.categories" :key="category" class="category-item">
                  {{ category }}
                </span>
              </div>
            </div>
          </li>
        </ul>
      </section>

      <!-- 已售出书籍 -->
      <section class="books-section">
        <h2>已售出书籍</h2>
        <ul>
          <li v-for="book in soldBooks" :key="book.id" class="book-item">
            <div class="book-cover">
              <img
                :src="book.cover_url || '@/assets/bg_image02.png'"
                alt="Book Cover"
                class="book-cover-img"
              />
            </div>
            <div class="book-info">
              <h3>{{ book.title }}</h3>
              <p>作者: {{ book.author }}</p>
              <p>售价: ￥{{ book.price }}</p>
              <div v-if="book.categories && book.categories.length" class="book-categories">
                <span v-for="category in book.categories" :key="category" class="category-item">
                  {{ category }}
                </span>
              </div>
            </div>
          </li>
        </ul>
      </section>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
.bookshelf-container {
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.publish-button {
  background: #4caf50;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #fff;
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.publish-button:hover {
  background-color: #388e3c;
}

.publish-button img {
  width: 24px;
  height: 24px;
}

.publish-text {
  display: none;
  margin-left: 8px;
  font-size: 16px;
  color: #fff;
}

.publish-button:hover .publish-text {
  display: inline;
}

.books-list-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.books-section {
  background: #f9f9f9;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.books-section h2 {
  margin-top: 0;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.book-item {
  display: flex;
  margin-bottom: 20px;
}

.book-cover {
  flex-shrink: 0;
  width: 80px;
  height: 120px;
  overflow: hidden;
  border-radius: 8px;
  margin-right: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.book-cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-info {
  flex-grow: 1;
}

.book-item h3 {
  font-size: 18px;
  color: #333;
  font-weight: bold;
  margin: 0 0 8px;
}

.book-item p {
  font-size: 14px;
  color: #666;
  margin: 4px 0;
}

.book-categories {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.category-item {
  background-color: #e0e0e0;
  color: #333;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.category-item:hover {
  background-color: #b0b0b0;
}

.error {
  color: red;
  text-align: center;
  margin-top: 20px;
}
</style>
