<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// 表单数据
const bookTitle = ref('');
const bookAuthor = ref('');
const bookPrice = ref<number | null>(null);
const bookDescription = ref('');
const bookImage = ref<File | null>(null);
const showModal = ref(false);
const modalMessage = ref('');
const router = useRouter();

// 提交发布表单
const handlePublish = async () => {
  if (!bookTitle.value || !bookAuthor.value || !bookPrice.value || !bookDescription.value) {
    showModal.value = true;
    modalMessage.value = '请填写完整的书籍信息！';
    return;
  }

  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      showModal.value = true;
      modalMessage.value = '用户未登录，请重新登录！';
      router.push('/login');
      return;
    }

    const formData = new FormData();
    formData.append('title', bookTitle.value);
    formData.append('author', bookAuthor.value);
    formData.append('price', bookPrice.value?.toString() || '');
    formData.append('description', bookDescription.value);
    if (bookImage.value) {
      formData.append('image', bookImage.value);
    }

    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/book/publish`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.code === 0) {
      showModal.value = true;
      modalMessage.value = '书籍发布成功！即将跳转到书架页面。';
      setTimeout(() => {
        showModal.value = false;
        router.push('/bookshelf');
      }, 2000);
    } else {
      showModal.value = true;
      modalMessage.value = response.data.msg || '发布失败，请稍后再试！';
    }
  } catch (error) {
    showModal.value = true;
    modalMessage.value = '发布失败，请稍后再试！';
    console.error('发布失败:', error);
  }
};
</script>

<template>
  <div class="publish-container">
    <!-- 标题 -->
    <h1 class="page-title">发布书籍</h1>

    <!-- 表单 -->
    <div class="form-card">
      <form @submit.prevent="handlePublish">
        <div class="form-group">
          <label for="title">书籍标题</label>
          <input v-model="bookTitle" type="text" id="title" placeholder="请输入书籍标题" />
        </div>
        <div class="form-group">
          <label for="author">作者</label>
          <input v-model="bookAuthor" type="text" id="author" placeholder="请输入书籍作者" />
        </div>
        <div class="form-group">
          <label for="price">价格</label>
          <input v-model="bookPrice" type="number" id="price" placeholder="请输入价格" />
        </div>
        <div class="form-group">
          <label for="description">描述</label>
          <textarea v-model="bookDescription" id="description" placeholder="请输入书籍描述"></textarea>
        </div>
        <div class="form-group">
          <label for="image">上传图片</label>
          <input @change="e => (bookImage.value = e.target.files[0])" type="file" id="image" accept="image/*" />
        </div>
        <button type="submit" class="publish-btn">发布</button>
      </form>
    </div>

    <!-- 弹窗 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <p>{{ modalMessage }}</p>
        <button @click="showModal = false" class="modal-btn">确定</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.publish-container {
  padding: 20px;
  background: linear-gradient(135deg, #f4f4f9, #e6e6fa);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
}

.form-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.publish-btn {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.publish-btn:hover {
  background-color: #45a049;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-btn {
  margin-top: 15px;
  padding: 10px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.modal-btn:hover {
  background: #45a049;
}
</style>
