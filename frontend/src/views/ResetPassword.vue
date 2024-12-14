<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import request from '@/utils/request'; // 导入封装的请求方法


const username = ref('');
const email = ref('');
const code = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isCodeSent = ref(false);
const router = useRouter();

const handleSendCode = async () => {
  errorMessage.value = '';
  if (!email.value || !username.value) {
    errorMessage.value = '用户名和邮箱不能为空';
    return;
  }

  const formData = new FormData();
  formData.append('email', email.value);
  formData.append('username', username.value);

  try {
    const response = await request.post('/api/user/code', formData);
    if (response.code === 0) {
      isCodeSent.value = true;
      successMessage.value = '验证码已发送，请检查邮箱';
    } else {
      errorMessage.value = response.msg || '发送验证码失败';
    }
  } catch (error) {
    errorMessage.value = '发送验证码失败，请稍后再试';
  }
};

const handleResetPassword = async () => {
  errorMessage.value = '';
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = '两次密码输入不一致';
    return;
  }

  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('email', email.value);
  formData.append('code', code.value);
  formData.append('new_password', newPassword.value);

  try {
    const response = await request.post('/api/user/reset', formData);

    if (response.code === 0) {
      successMessage.value = '密码重置成功！';
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      errorMessage.value = response.msg || '密码重置失败';
    }
  } catch (error) {
    errorMessage.value = '密码重置失败，请稍后再试';
  }
};

</script>

<template>
  <div class="reset-password-container">
    <form @submit.prevent="handleResetPassword" class="reset-form">
      <h2>重置密码</h2>
      
      <div class="form-group">
        <label for="username">用户名：</label>
        <input v-model="username" type="text" id="username" placeholder="请输入用户名" required />
      </div>
      
      <div class="form-group">
        <label for="email">邮箱：</label>
        <input v-model="email" type="email" id="email" placeholder="请输入邮箱" required />
      </div>
      
      <div class="form-group">
        <label for="code">验证码：</label>
        <div class="code-container">
          <input v-model="code" type="text" id="code" placeholder="请输入验证码" required />
          <button type="button" @click="handleSendCode" :disabled="isCodeSent" class="send-code-btn">
            发送验证码
          </button>
        </div>
      </div>
      
      <div class="form-group">
        <label for="newPassword">新密码：</label>
        <input v-model="newPassword" type="password" id="newPassword" placeholder="请输入新密码" required />
      </div>
      
      <div class="form-group">
        <label for="confirmPassword">确认密码：</label>
        <input v-model="confirmPassword" type="password" id="confirmPassword" placeholder="确认密码" required />
      </div>
      
      <button type="submit" class="submit-btn">重置密码</button>
      
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f6f9;
  padding: 20px;
}

.reset-form {
  background: #ffffff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

label {
  display: block;
  font-size: 16px;
  color: #555;
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
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
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.code-container {
  display: flex;
  align-items: center;
}

.send-code-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  font-size: 14px;
  margin-left: 10px;
  cursor: pointer;
}

.send-code-btn:hover {
  background-color: #1976D2;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

.success {
  color: green;
  font-size: 14px;
  margin-top: 10px;
}

.submit-btn {
  background-color: #4CAF50;
}

.submit-btn:hover {
  background-color: #45a049;
}
</style>
