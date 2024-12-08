<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

// 表单字段
const bookTitle = ref('');
const bookAuthor = ref('');
const bookPrice = ref<number | null>(null);
const bookDescription = ref('');
const bookImage = ref<File | null>(null);
const errorMessage = ref('');
const successMessage = ref('');
const isLoggedIn = ref(false);  // 登录状态
const activeTab = ref('publish'); // 默认是发布书籍
const books = ref([]);

// 路由实例
const router = useRouter();
const route = useRoute();

// 获取数据函数（例如获取售出书籍数据）
const fetchSoldBooks = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/books/sold`);
    books.value = response.data.books || [];
  } catch (error) {
    console.error('Failed to fetch sold books:', error);
  }
};

// 监听路由变化，更新视图
watch(route, () => {
  if (activeTab.value === 'sold') {
    fetchSoldBooks();
  }
});

// 页面初始化，检查登录状态
onMounted(() => {
  const user = localStorage.getItem('user');  // 从 localStorage 获取登录状态
  if (user) {
    isLoggedIn.value = true;  // 如果有用户信息，设置为已登录
  } else {
    isLoggedIn.value = false;  // 未登录
    router.push('/login');  // 重定向到登录页面
  }

  // 如果当前选项卡是已售出书籍，加载数据
  if (activeTab.value === 'sold') {
    fetchSoldBooks();
  }
});

// 提交发布表单
const handlePublish = async () => {
  if (!bookTitle.value || !bookAuthor.value || !bookPrice.value || !bookDescription.value) {
    errorMessage.value = '请填写完整的书籍信息';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('title', bookTitle.value);
    formData.append('author', bookAuthor.value);
    formData.append('price', bookPrice.value.toString());
    formData.append('description', bookDescription.value);
    if (bookImage.value) {
      formData.append('image', bookImage.value);
    }

    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/book/publish`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.code === 0) {
      successMessage.value = '书籍发布成功！';
      errorMessage.value = '';
      // 清空表单
      bookTitle.value = '';
      bookAuthor.value = '';
      bookPrice.value = null;
      bookDescription.value = '';
      bookImage.value = null;
    } else {
      errorMessage.value = response.data.msg || '发布失败，请稍后再试';
    }
  } catch (error) {
    errorMessage.value = '发布失败，请稍后再试';
    console.error('发布失败:', error);
  }
};
</script>

<template>
  <div class="publish-container">
    <div class="tabs">
      <button
        :class="{ active: activeTab === 'publish' }"
        @click="activeTab = 'publish'"
      >
        发布书籍
      </button>
      <button
        :class="{ active: activeTab === 'sold' }"
        @click="activeTab = 'sold'; fetchSoldBooks();"
      >
        已售出书籍
      </button>
    </div>

    <!-- 发布书籍表单 -->
    <div v-if="activeTab === 'publish' && isLoggedIn" class="form-container">
      <h2>发布新书</h2>
      <form @submit.prevent="handlePublish">
        <div class="form-group">
          <label for="title">书籍标题</label>
          <input
            v-model="bookTitle"
            type="text"
            id="title"
            placeholder="请输入书籍标题"
          />
        </div>
        <div class="form-group">
          <label for="author">作者</label>
          <input
            v-model="bookAuthor"
            type="text"
            id="author"
            placeholder="请输入书籍作者"
          />
        </div>
        <div class="form-group">
          <label for="price">价格</label>
          <input
            v-model="bookPrice"
            type="number"
            id="price"
            placeholder="请输入价格"
          />
        </div>
        <div class="form-group">
          <label for="description">描述</label>
          <textarea
            v-model="bookDescription"
            id="description"
            placeholder="请输入书籍描述"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="image">上传图片</label>
          <input
            @change="e => (bookImage = e.target.files[0])"
            type="file"
            id="image"
            accept="image/*"
          />
        </div>
        <button type="submit">发布</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
      </form>
    </div>

    <!-- 已售出书籍列表 -->
    <div v-if="activeTab === 'sold'" class="books-list">
      <h2>已售出书籍</h2>
      <ul>
        <li v-for="book in books" :key="book.id">
          <h3>{{ book.title }}</h3>
          <p>作者: {{ book.author }}</p>
          <p>售价: ￥{{ book.price }}</p>
        </li>
      </ul>
    </div>

    <!-- 未登录提示 -->
    <div v-else-if="activeTab === 'publish' && !isLoggedIn" class="login-prompt">
      <p>请先登录才能发布书籍。</p>
    </div>
  </div>
</template>

<style scoped>
.publish-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  margin: 0 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.form-container, .books-list {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
}

.success {
  color: green;
}

.login-prompt {
  text-align: center;
  font-size: 18px;
  color: red;
}
</style>
