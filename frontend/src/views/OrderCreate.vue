<template>
  <div class="order-create">
    <div class="container">
      <h1 class="page-title">创建订单</h1>

      <!-- 书籍信息展示 -->
      <div class="book-info">
        <h3>书籍信息</h3>
        <div class="info-group">
          <label for="bookId">书籍 ID:</label>
          <span>{{ form.book_id }}</span>
        </div>

        <div class="info-group">
          <label for="bookTitle">书名:</label>
          <span>{{ bookTitle }}</span>
        </div>

        <div class="info-group">
          <label for="sellerName">卖家姓名:</label>
          <span>{{ sellerName }}</span>
        </div>

        <div class="info-group">
          <label for="bookPrice">价格:</label>
          <span>{{ bookPrice }} 元</span>
        </div>
      </div>

      <!-- 确认订单部分 -->
      <div class="confirm-section">
        <h3>确认订单</h3>
        <p>您即将购买上述书籍，请确认订单信息是否正确。</p>

        <div class="buttons">
          <button @click="cancelOrder" class="cancel-button">取消</button>
          <button @click="createOrder" class="confirm-button">确认创建订单</button>
        </div>
      </div>
    </div>

    <!-- 弹窗显示 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>订单创建成功</h3>
        <button @click="goToOrderList" class="modal-button">返回订单列表</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import request from '@/utils/request'; // 使用封装的 Axios 实例

// 定义变量
const router = useRouter();
const route = useRoute();
const form = ref({ book_id: null });
const bookTitle = ref('');
const sellerName = ref('');
const bookPrice = ref('');
const showModal = ref(false); // 弹窗显示状态
const errorMessage = ref('');  // 用于显示错误信息

// 获取查询参数
const bookId = route.query.bookId as string;
const bookTitleQuery = route.query.bookTitle as string;
const bookPriceQuery = route.query.bookPrice as string;
const publisherIdQuery = route.query.publisherId as string; // 获取 publisherId

// 确保参数存在
if (bookId) {
  form.value.book_id = bookId;
}
if (bookTitleQuery) {
  bookTitle.value = bookTitleQuery;
}
if (bookPriceQuery) {
  bookPrice.value = bookPriceQuery;
}

// 获取卖家姓名
const fetchSellerName = async (sellerId: string) => {
  try {
    const response = await request.get(`/api/user/name/${sellerId}`);
    sellerName.value = response.username;  // 设置卖家姓名
  } catch (error) {
    console.error('获取卖家信息失败:', error);
  }
};

// 在组件挂载时获取卖家信息
onMounted(() => {
  if (publisherIdQuery) {
    fetchSellerName(publisherIdQuery); // 异步获取卖家姓名
  }
});

// 检查用户登录状态
const checkLogin = () => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    errorMessage.value = '用户未登录，请重新登录。';
    router.push('/login');
    return false;
  }
  return true;
};

const createOrder = async () => {
  if (!checkLogin()) return;  // 如果用户未登录，停止创建订单

  const token = localStorage.getItem('auth_token');
  if (!token) {
    alert('用户未登录，请重新登录');
    return;
  }

  const formData = new FormData();
  formData.append('book_id', form.value.book_id);
  // 如果接口需要其他字段，可以在此处继续添加

  try {
    const response = await request.post(
      '/api/order/buy',
      formData, 
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    if (response.code === 0) {
      // 订单创建成功，显示弹窗
      showModal.value = true; // 弹窗显示
    } else {
      alert(`订单创建失败: ${response.msg}`);
    }
  } catch (error) {
    console.error('创建订单失败:', error);
    alert('创建订单时发生错误，请稍后重试');
  }
};

// 取消订单
const cancelOrder = () => {
  router.push('/bookList'); // 返回书籍列表
};

// 返回订单列表
const goToOrderList = () => {
  router.push('/orderList');
};
</script>

<style scoped>
.order-create {
  background: linear-gradient(135deg, #f4f4f9, #e6e6fa);
  min-height: 100vh;
  padding: 20px;
}

.container {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
}

.book-info {
  margin-bottom: 30px;
}

.book-info h3 {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 10px;
}

.info-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.info-group label {
  font-size: 1rem;
  color: #555;
}

.info-group span {
  font-size: 1rem;
  color: #333;
}

.confirm-section {
  text-align: center;
}

.confirm-section h3 {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 20px;
}

.confirm-section p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: space-around;
}

.cancel-button, .confirm-button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  width: 45%;
}

.cancel-button {
  background-color: #d9534f;
  color: white;
  border: none;
}

.cancel-button:hover {
  background-color: #c9302c;
}

.confirm-button {
  background-color: #5bc0de;
  color: white;
  border: none;
}

.confirm-button:hover {
  background-color: #31b0d5;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  width: 300px;
}

.modal-button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-button:hover {
  background-color: #218838;
}
</style>
