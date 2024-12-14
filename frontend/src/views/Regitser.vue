<template>
  <div class="home-container">
    <div class="illustration">
      <img src="../assets/bg_img01.jpg" alt="illustration" />
    </div>
    <div class="content">
      <div class="login-message">
        <h2>注册</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="username">用户名:</label>
            <input v-model="user.username" type="text" id="username" placeholder="请输入用户名" required />
          </div>
          <div class="form-group">
            <label for="password">密码:</label>
            <input v-model="user.password" type="password" id="password" placeholder="请输入密码" required />
          </div>
          <div class="form-group">
            <label for="email">邮箱:</label>
            <input v-model="user.email" type="email" id="email" placeholder="请输入邮箱" required />
            <button type="button" @click="sendVerificationCode" :disabled="isSendingCode">
              获取验证码
            </button>
          </div>
          <div class="form-group">
            <label for="code">验证码:</label>
            <input v-model="user.code" type="text" id="code" placeholder="请输入验证码" required />
          </div>
          <button type="submit">注册</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>

    <!-- 装饰图案 -->
    <img class="leaf1" src="../assets/green.svg" alt="leaf decoration" />
    <img class="leaf2" src="../assets/green.svg" alt="leaf decoration" />

    <!-- 注册成功弹窗 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h2>注册成功!</h2>
        <p>您已经成功注册，点击下面的按钮进行登录。</p>
        <button @click="redirectToLogin">去登录</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const user = reactive({
  username: '',
  password: '',
  email: '', // 邮箱字段
  code: '',  // 验证码字段
});

const errorMessage = ref<string>('');
const showModal = ref(false); // 控制模态框显示
const isSendingCode = ref(false); // 控制发送验证码按钮的状态

const router = useRouter();

// 发送验证码请求
const sendVerificationCode = async () => {
  if (!user.email) {
    errorMessage.value = '请输入邮箱地址';
    return;
  }
  
  isSendingCode.value = true;
  try {
    const formData = new FormData();
    formData.append('username', user.username);
    formData.append('email', user.email);
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/user/code`, formData ,{
      'Content-Type': 'multipart/form-data',
    });

    if (response.data.code === 0) {
      alert('验证码已发送，请查收邮箱！');
    } else {
      errorMessage.value = response.data.msg;
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.msg || '发送验证码失败';
  } finally {
    isSendingCode.value = false;
  }
};

// 提交注册请求
const handleSubmit = async () => {
  if (!user.code) {
    errorMessage.value = '请输入验证码';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('username', user.username);
    formData.append('password',user.password)
    formData.append('email', user.email);
    formData.append('code', user.code); // 加上验证码字段

    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/user/register`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.code === 0) {
      showModal.value = true; // 显示注册成功模态框
    } else {
      errorMessage.value = response.data.msg;
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.msg || '注册失败';
  }
};

const closeModal = () => {
  showModal.value = false;
};

const redirectToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.home-container {
  padding: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5, #d1e0e0), url('../assets/background.svg');
  background-size: cover;
  background-position: center;
  position: relative;
}

.illustration {
  position: absolute;
  left: 8%;
  top: 45%;
  transform: translateY(-50%);
}

.illustration img {
  width: 488px; /* 控制插画大小 */
  height: auto;
}

.content {
  margin-left: 488px; /* 右移注册框，使其不覆盖插画 */
  width: 100%;
  max-width: 400px;
  margin-top: -20px;
}

.login-message {
  background-color: rgba(255, 255, 255, 0.8); /* 半透明背景 */
  color: #333;
  padding: 30px 50px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
  margin: 10px 20px;
  position: relative;
}

h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
}

.form-group {
  margin-bottom: 25px;
  text-align: left;
}

label {
  display: block;
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
  outline: none;
}

input::placeholder {
  color: #aaa;
}

button {
  width: 100%;
  padding: 14px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }

  .illustration {
    display: none; /* 移动端不显示插画 */
  }

  .content {
    margin-left: 0;
  }

  .login-message {
    padding: 20px;
    max-width: 90%;
  }

  h2 {
    font-size: 24px;
  }

  button {
    font-size: 16px;
  }

  input {
    padding: 10px;
  }

  .leaf1, .leaf2 {
    width: 150px;
    height: 150px;
  }
}

/* 装饰图案 */
.leaf1, .leaf2 {
  position: absolute;
  top: 30px;
  z-index: 1;
  opacity: 0.6;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

.leaf1 {
  left: 10%;
  width: 180px;
  height: 180px;
  animation: floatLeaf1 6s infinite;
}

.leaf2 {
  right: 10%;
  width: 200px;
  height: 200px;
  animation: floatLeaf2 8s infinite;
}

/* 动画效果 */
@keyframes floatLeaf1 {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(15deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(20px) rotate(-15deg);
  }
  100% {
    transform: translateY(0) rotate(0deg);
  }
}

@keyframes floatLeaf2 {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-30px) rotate(-10deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(30px) rotate(10deg);
  }
  100% {
    transform: translateY(0) rotate(0deg);
  }
}

/* Modal */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  max-width: 400px;
  text-align: center;
}

.modal-content {
  font-family: 'Arial', sans-serif;
  color: #333;
}

.close {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
  color: #333;
}

button {
  width: auto;
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  background-color: #45a049;
}
</style>
