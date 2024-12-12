<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import request from '@/utils/request'; // 使用封装的 Axios 实例
import { useRouter } from 'vue-router';
import Search from '@/components/Search.vue';
import type { Book } from '@/types';

// 书籍数据及搜索过滤
const books = ref<Book[]>([]);
const searchQuery = ref('');
const selectedCategory = ref(''); // 当前选择的类别
const loading = ref(true);
const router = useRouter();

// 动态提取类别选项
const categories = computed(() => {
  const allCategories = books.value.flatMap((book) => book.categories);
  return Array.from(new Set(allCategories)); // 去重
});

// 联合过滤
const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  const category = selectedCategory.value;

  return books.value.filter((book) => {
    const matchesQuery =
      !query ||
      book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query);

    const matchesCategory =
      !category || book.categories.includes(category);

    return matchesQuery && matchesCategory;
  });
});

// 获取书籍数据
const fetchBooks = async () => {
  try {
    const response = await request.get('/api/book/list');
    books.value = response.data;
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
const viewBookDetail = (bookId: number) => {
  router.push(`/book/${bookId}`);
};
</script>

<template>
  <div class="book-list">
    <div class="container">
      <!-- 页标题 -->
      <h1 class="page-title">查找你喜爱的图书吧！</h1>

      <!-- 搜索框 -->
      <Search v-model="searchQuery" />

      <!-- 类别过滤 -->
      <div class="category-filter">
        <label for="category">按类别筛选：</label>
        <select id="category" v-model="selectedCategory">
          <option value="">全部</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- 书籍列表 -->
      <div v-if="!loading" class="book-grid">
        <div
          v-for="book in filteredBooks"
          :key="book.id"
          class="book-card"
          @click="viewBookDetail(book.id)"
        >
          <img
            v-if="book.cover_url"
            :src="book.cover_url"
            alt="Book Cover"
            class="book-cover"
          />
          <h2 class="book-title">{{ book.title }}</h2>
          <p class="book-author">作者: {{ book.author }}</p>
          <div class="book-categories">
            分类：
            <span v-for="(category, index) in book.categories" :key="index" class="category">
              {{ category }}
            </span>
          </div>
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

.category-filter {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* 动态调整列数 */
  gap: 20px; /* 保持卡片之间的间距 */
  width: 100%;
  justify-content: center; /* 确保内容居中 */
}

.book-card {
  max-width: 300px; /* 限制卡片的最大宽度 */
  width: 100%; /* 自适应网格列的宽度 */
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  box-sizing: border-box; /* 确保内外边距不会影响宽度计算 */
}

.book-card img {
  display: block; /* 确保图片不会溢出父级容器 */
  margin: 0 auto; /* 图片居中 */
  width: 120px; /* 限制图片的宽度 */
  height: auto;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
}

.book-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #222;
  word-wrap: break-word; /* 防止标题太长时溢出 */
}

.book-author,
.book-categories {
  font-size: 1rem;
  margin-bottom: 5px;
  color: #555;
}

.book-categories {
  font-size: 0.9rem;
  color: #777;
}

.category {
  display: inline-block;
  background: #eef;
  padding: 3px 8px;
  margin: 2px;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #334;
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