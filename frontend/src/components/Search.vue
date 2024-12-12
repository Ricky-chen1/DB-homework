<script setup lang="ts">
import { ref, defineEmits } from 'vue';

// 搜索输入内容
const searchQuery = ref('');
const emit = defineEmits(['update:modelValue']);

// 触发搜索的函数
const triggerSearch = () => {
  emit('update:modelValue', searchQuery.value); // 向父组件同步搜索内容
};

// 按下键盘时监听回车键
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    triggerSearch();
  }
};
</script>


<template>
  <div class="search-bar">
    <!-- 搜索输入框 -->
    <input
      type="text"
      class="search-input"
      v-model="searchQuery"
      placeholder="输入书名或者作者搜索..."
      @keydown="handleKeyDown"
    />
    <!-- 搜索按钮 -->
    <button class="search-button" @click="triggerSearch">
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

.iconfont {
  font-size: 20px;
  color: white;
}
</style>
