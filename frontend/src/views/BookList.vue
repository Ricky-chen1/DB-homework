<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Search from '@/components/Search.vue';

// 书籍数据及搜索过滤
const books = ref([]);
const searchQuery = ref('');
const loading = ref(true);
const router = useRouter();

const filteredBooks = computed(() => {
  if (!searchQuery.value.trim()) {
    return books.value;
  }
  return books.value.filter((book) =>
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

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
  fetchBooks();
});

// 查看书籍详情
const viewBookDetail = (bookId: string) => {
  router.push(`/book/${bookId}`);
};
</script>

<template>
  <div class="book-list">
    <div class="container">
      <!-- 页标题 -->
      <h1 class="page-title">二手书籍列表</h1>

      <!-- 搜索框 -->
      <Search v-model="searchQuery" />

      <!-- 书籍列表 -->
      <div v-if="!loading" class="book-grid">
        <div v-for="book in filteredBooks" :key="book.id" class="book-card" @click="viewBookDetail(book.id)">
          <img 
            v-if="book.image" 
            :src="book.image" 
            alt="Book Cover" 
            class="book-cover" 
          />
          <h2 class="book-title">{{ book.title }}</h2>
          <p class="book-author">作者: {{ book.author }}</p>
          <p class="book-price">价格: ¥{{ book.price }}</p>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else-if="loading" class="loading-message">
        正在加载图书数据，请稍候...
      </div>

      <!-- 无书籍提示 -->
      <div v-else class="no-books-message">
        暂无图书信息，试试其他搜索条件。
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-list {
  padding: 20px;
  background: linear-gradient(135deg, #f4f4f9, #e6e6fa);
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
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
  font-weight: bold;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  width: 100%;
}

.book-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
}

.book-cover {
  width: 120px;
  height: auto;
  margin-bottom: 15px;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.book-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #222;
}

.book-author,
.book-price {
  font-size: 1rem;
  margin-bottom: 5px;
  color: #555;
}

.loading-message,
.no-books-message {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  margin-top: 30px;
  padding: 20px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}
</style>
