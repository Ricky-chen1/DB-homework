<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// 表单数据
const bookTitle = ref('');
const bookAuthor = ref('');
const bookPrice = ref<number | null>(null);
const bookDescription = ref('');
const selectedCategories = ref<string[]>([]);
const bookImage = ref<File | null>(null);
const showModal = ref(false);
const modalMessage = ref('');
const router = useRouter();

// 封面图片预览
const previewImage = ref<string | null>(null);

// 类别选项
const categoryOptions = [
  '教育', '教材', '外语', '考试', '中小学用书', '工具书',
  '小说', '文艺', '文学', '传记', '艺术', '摄影'
];

// 提交发布表单
const handlePublish = async () => {
  if (!bookTitle.value || !bookAuthor.value || !bookPrice.value || !bookDescription.value || selectedCategories.value.length === 0) {
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
    // 直接将多个类别值作为同一字段的多个项传递
    selectedCategories.value.forEach(category => {
      formData.append('categories', category);  // 以数组形式传递
    });
    if (bookImage.value) {
      formData.append('cover', bookImage.value);
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

// 封面图片预览
const handleImageChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) {
    bookImage.value = file;
    const reader = new FileReader();
    reader.onload = () => {
      previewImage.value = reader.result as string;
    };
    reader.readAsDataURL(file);
  }
};

// 选择类别
const toggleCategory = (category: string) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter(c => c !== category);
  } else {
    selectedCategories.value.push(category);
  }
};

// 取消选择封面图片
const removeImage = () => {
  bookImage.value = null;
  previewImage.value = null;
};
</script>

<template>
  <div class="publish-container">
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

        <!-- 类别选择 -->
        <div class="form-group categories">
          <label>选择类别</label>
          <div class="category-options">
            <div 
              v-for="category in categoryOptions" 
              :key="category" 
              class="category-option" 
              :class="{'selected': selectedCategories.includes(category)}"
              @click="toggleCategory(category)">
              <span>{{ category }}</span>
              <span v-if="selectedCategories.includes(category)" class="remove-category">x</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="image">上传封面图片</label>
          <input @change="handleImageChange" type="file" id="cover" accept="image/*" />
        </div>

        <!-- 图片预览 -->
        <div v-if="previewImage" class="image-preview">
          <img :src="previewImage" alt="封面图片预览" />
          <span @click="removeImage" class="remove-image">x</span>
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
/* 全局背景色和布局 */
.publish-container {
  padding: 40px;
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
  font-family: 'Arial', sans-serif;
}

/* 表单卡片样式 */
.form-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 700px;
}

/* 表单输入项样式 */
.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 1.1rem;
  color: #4e4e4e;
}

input,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 1rem;
  font-family: 'Arial', sans-serif;
  transition: border-color 0.3s;
}

input:focus,
textarea:focus {
  border-color: #4caf50;
  outline: none;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

/* 类别选择 */
.categories {
  margin-top: 10px;
}

.category-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-option {
  padding: 8px 15px;
  background-color: #f4f4f9;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
}

.category-option.selected {
  background-color: #4caf50;
  color: white;
}

.remove-category {
  margin-left: 8px;
  font-size: 1.2rem;
  cursor: pointer;
  color: #f44336;
}

/* 图片预览样式 */
.image-preview {
  margin-top: 20px;
  text-align: center;
  position: relative;
}

.image-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 12px;
  object-fit: contain;
  border: 2px solid #ddd;
  padding: 5px;
}

.remove-image {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  padding: 5px;
  cursor: pointer;
}

/* 发布按钮样式 */
.publish-btn {
  width: 100%;
  padding: 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.publish-btn:hover {
  background-color: #45a049;
}

/* 弹窗样式 */
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
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
}

.modal-btn {
  margin-top: 20px;
  padding: 12px 25px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.modal-btn:hover {
  background: #45a049;
}
</style>
