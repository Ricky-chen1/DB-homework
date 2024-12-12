<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import request from '@/utils/request';
import type { Order } from '@/types/order';
import type { Book } from '@/types/book';
import type { User } from '@/types/user';

// 初始化响应式数据
const orderDetail = ref<Order | null>(null);

const route = useRoute();
const orderId = ref<number | null>(null);

if (route.params.orderId) {
  const parsedId = Number(route.params.orderId);
  if (!isNaN(parsedId)) {
    orderId.value = parsedId;
  } else {
    console.error('Invalid orderId: Not a number');
  }
} else {
  console.error('Invalid orderId: Missing in route params');
}


// 获取订单详情
const fetchOrderDetail = async () => {
  if (!orderId.value) {
    console.error('Invalid orderId');
    return;
  }

  const token = localStorage.getItem('auth_token');
  if (!token) {
    console.error('No auth token found');
    return;
  }

  try {
    // 获取订单信息
    const orderResponse = await request.get(`/api/order/${orderId.value}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Order Response:', orderResponse);
    if (orderResponse.code === 0) {
      const order = orderResponse.data;

      // 获取书籍信息
      const bookResponse = await request.get<Book>(`/api/book/${order.book_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // 获取卖家信息
      const sellerResponse = await request.get<User>(`/api/user/name/${order.seller_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // 合并订单信息
      order.book_title = bookResponse.data.title;
      order.seller_name = sellerResponse.username;

      orderDetail.value = order;
    } else {
      console.error('Failed to fetch order data:', orderResponse.data.msg);
    }
  } catch (error) {
    console.error('获取订单详情失败:', error);
  }
};

// 状态映射
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

// 退款订单
const refundOrder = async (orderId: number) => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    console.error('No auth token found');
    return;
  }

  try {
    const response = await request.post('/api/order/cancel', { order_id: orderId }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.code === 0) {
      orderDetail.value!.status = 'cancelled'; // 假设退款后订单变为取消状态
    } else {
      console.error('退款失败:', response.msg);
    }
  } catch (error) {
    console.error('退款订单失败:', error);
  }
};

// 页面加载时获取订单详情
onMounted(fetchOrderDetail);
</script>

<template>
  <div class="order-detail">
    <div class="container">
      <h2 class="page-title">订单详情</h2>
      <div v-if="orderDetail">
        <div class="order-info">
          <h3 class="book-title">
            <span class="icon">📚</span> {{ orderDetail.book_title }}
          </h3>
          <p class="seller-name">
            <span class="label">卖家:</span> {{ orderDetail.seller_name }}
          </p>
          <p class="order-status">
            <span class="label">状态:</span> 
            <span :class="`status-${orderDetail.status}`">
              {{ orderStatusText(orderDetail.status) }}
            </span>
          </p>
          <p class="order-price">
            <span class="label">价格:</span> ¥{{ orderDetail.price }}
          </p>
          <p class="order-created">
            <span class="label">创建时间:</span> {{ orderDetail.created_at }}
          </p>
          <p class="order-updated">
            <span class="label">更新时间:</span> {{ orderDetail.updated_at }}
          </p>
        </div>

        <!-- 显示退款或取消按钮 -->
        <div v-if="orderDetail.status === 'paid'" class="action-buttons">
          <button class="refund-button" @click="refundOrder(orderDetail.id)">
            退款
          </button>
        </div>
      </div>
      <div v-else class="loading">
        <p>加载订单详情中...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-detail {
  padding: 30px;
  background: #f9f9f9;
}

.container {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.8rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.book-title {
  font-size: 1.6rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.book-title .icon {
  margin-right: 8px;
}

.seller-name,
.order-status,
.order-price,
.order-created,
.order-updated {
  font-size: 1.2rem;
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  color: #555;
  margin-right: 8px;
}

.order-status .status-paid {
  color: #4caf50;
}

.order-status .status-pending {
  color: #ff9800;
}

.order-status .status-cancelled {
  color: #f44336;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.refund-button {
  padding: 10px 20px;
  background-color: #ff9800;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.refund-button:hover {
  background-color: #f57c00;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  margin-top: 50px;
}
</style>
