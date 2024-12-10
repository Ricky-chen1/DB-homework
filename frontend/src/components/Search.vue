<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useBackendDataStore } from '@/stores/data';

// 引用 Pinia store
const store = useBackendDataStore();
const searchQuery = ref('');

const performSearch = async () => {
  if (!searchQuery.value.trim()) return;

  try {
    // 发送搜索请求到后端
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/book/search`, {
      params: {
        query: searchQuery.value.trim(),
      },
    });

    // 将后端返回数据存入 Pinia store
    store.setBackendData(response.data);
  } catch (error) {
    console.error('搜索请求失败:', error);
  }
};
</script>

<template>
  <div class="search-bar">
    <input 
      type="text" 
      class="search-input" 
      v-model="searchQuery" 
      placeholder="Search books by title or category..."
    />
    <button class="search-button" @click="performSearch">
      <!-- 使用 iconfont 提供的搜索图标 -->
      <i class="iconfont icon-sousuo"></i>
    </button>
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  max-width: 600px;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 5px 0 0 5px;
  outline: none;
  font-size: 1rem;
}

.search-input:focus {
  border-color: #007bff;
}

.search-button {
  background-color: #007bff;
  border: none;
  padding: 10px 15px;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  background-color: #0056b3;
}

.iconfont {
  font-size: 20px;
  color: white;
}
</style>

<!-- 引入 iconfont 样式 -->
<link rel="stylesheet" href="https://at.alicdn.com/t/c/font_4756601_9mxxkv4q5qo.css">
