<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import request from '@/utils/request';
import type { Order } from '@/types/order';
import type { Book } from '@/types/book';
import type { User } from '@/types/user';

// 订单数据及加载状态
const orderList = ref<Order[]>([]);
const booksMap = ref<Map<number, Book>>(new Map());
const sellersMap = ref<Map<number, User>>(new Map());
const loading = ref(true);
const errorMessage = ref<string | null>(null);
const router = useRouter();

// 获取订单列表
const fetchOrderList = async () => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    errorMessage.value = '用户未登录，请重新登录。';
    loading.value = false;
    return;
  }

  try {
    // 获取订单列表
    const orderResponse = await request.get<GetOrderListResponse>('/api/order/list', {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (orderResponse.code === 0) {
      const orders = orderResponse.data;
      // 获取每个订单的书籍信息和卖家信息
      for (let order of orders) {
        // 获取书籍信息
        if (!booksMap.value.has(order.book_id)) {
          const bookResponse = await request.get<Book>(`/api/book/${order.book_id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          booksMap.value.set(order.book_id, bookResponse);
        }

        // 获取卖家信息
        if (!sellersMap.value.has(order.seller_id)) {
          const sellerResponse = await request.get<User>(`/api/user/name/${order.seller_id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          sellersMap.value.set(order.seller_id, sellerResponse);
        }
      }

      orderList.value = orders;
    } else {
      errorMessage.value = `获取订单列表失败: ${orderResponse.msg}`;
    }
  } catch (error) {
    console.error('请求订单列表失败:', error);
    errorMessage.value = '获取订单列表失败，请稍后重试。';
  } finally {
    loading.value = false;
  }
};

// 页面加载时获取订单列表
onMounted(fetchOrderList);

// 状态映射到中文
const orderStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待支付';
    case 'paid':
      return '已支付';
    case 'cancelled':
      return '已取消';
    default:
      return '未知状态';
  }
};

// 支付订单
const payOrder = async (orderId: number) => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    errorMessage.value = '用户未登录，请重新登录。';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('order_id', orderId.toString());

    const response = await request.post('/api/order/pay', formData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      // 更新订单状态为已支付
      const updatedOrder = orderList.value.find(order => order.id === orderId);
      if (updatedOrder) updatedOrder.status = response.data.status;
    } else {
      errorMessage.value = `支付失败: ${response.msg}`;
    }
  } catch (error) {
    console.error('支付订单失败:', error);
    errorMessage.value = '支付失败，请稍后重试。';
  }
};

// 取消订单
const cancelOrder = async (orderId: number) => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    errorMessage.value = '用户未登录，请重新登录。';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('order_id', orderId.toString());

    const response = await request.post('/api/order/cancel', formData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      // 更新订单状态为已取消
      const updatedOrder = orderList.value.find(order => order.id === orderId);
      if (updatedOrder) updatedOrder.status = response.data.status;
    } else {
      errorMessage.value = `取消订单失败: ${response.msg}`;
    }
  } catch (error) {
    console.error('取消订单失败:', error);
    errorMessage.value = '取消订单失败，请稍后重试。';
  }
};

// 退款订单
const refundOrder = async (orderId: number) => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    errorMessage.value = '用户未登录，请重新登录。';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('order_id', orderId.toString());

    const response = await request.post('/api/order/cancel', formData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      // 更新订单状态为已退款
      const updatedOrder = orderList.value.find(order => order.id === orderId);
      if (updatedOrder) updatedOrder.status = response.data.status;
    } else {
      errorMessage.value = `退款失败: ${response.msg}`;
    }
  } catch (error) {
    console.error('退款订单失败:', error);
    errorMessage.value = '退款失败，请稍后重试。';
  }
};

// 查看订单详情
const viewOrderDetail = (orderId: number) => {
  router.push(`/order/${orderId}`);
};
</script>
<template>
  <div class="order-list">
    <div class="container">
      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-message">
        正在加载订单列表，请稍候...
      </div>

      <!-- 订单列表 -->
      <div v-if="!loading && orderList.length" class="order-items">
        <div v-for="order in orderList" :key="order.id" class="order-item" @click="viewOrderDetail(order.id)">
          <div class="book-cover" v-if="booksMap.has(order.book_id)">
            <img :src="booksMap.get(order.book_id)?.cover" alt="Book Cover" />
          </div>
          <div class="order-info">
            <h3 class="book-title" v-if="booksMap.has(order.book_id)">
              {{ booksMap.get(order.book_id)?.title }}
            </h3>
            <p class="seller-name" v-if="sellersMap.has(order.seller_id)">
              <strong>卖家:</strong> {{ sellersMap.get(order.seller_id)?.username }}
            </p>
            <p class="order-status">{{ orderStatusText(order.status) }}</p>
            <p class="order-price">¥{{ order.price }}</p>
            <!-- 仅显示待支付订单的操作按钮 -->
            <div v-if="order.status === 'pending'" class="action-buttons">
              <button class="pay-button" @click.stop="payOrder(order.id)">
                支付
              </button>
              <button class="cancel-button" @click.stop="cancelOrder(order.id)">
                取消
              </button>
            </div>
            <!-- 显示已支付订单的退款按钮 -->
            <div v-if="order.status === 'paid'" class="action-buttons">
              <button class="refund-button" @click.stop="refundOrder(order.id)">
                退款
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 没有订单时的提示 -->
      <div v-if="!loading && orderList.length === 0" class="no-orders">
        当前没有订单。
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-list {
  display: flex;
  justify-content: center;
  align-items: flex-start;
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

.order-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background-color: #f9f9f9;
  cursor: pointer;
}

.book-cover img {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.order-info {
  flex-grow: 1;
  margin-left: 15px;
}

.book-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.seller-name {
  font-size: 1rem;
  color: #555;
  margin-bottom: 10px;
}

.order-status {
  font-size: 0.9rem;
  color: #777;
}

.order-price {
  font-size: 1.1rem;
  color: #333;
  margin-top: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.pay-button, .cancel-button, .refund-button {
  padding: 8px 15px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  width: 100px;
}

.pay-button {
  background-color: #4caf50;
  color: white;
}

.pay-button:hover {
  background-color: #388e3c;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}

.cancel-button:hover {
  background-color: #d32f2f;
}

.refund-button {
  background-color: #ff9800;
  color: white;
}

.refund-button:hover {
  background-color: #f57c00;
}

.loading-message, .error-message, .no-orders {
  font-size: 1.2rem;
  color: #888;
  text-align: center;
}

.error-message {
  color: #d9534f;
}

.loading-message {
  font-size: 1.5rem;
  color: #333;
}

.no-orders {
  font-size: 1.2rem;
  color: #777;
}
</style>
