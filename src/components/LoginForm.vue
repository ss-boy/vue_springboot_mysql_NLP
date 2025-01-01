<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div>
        <label for="username">Username</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input v-model="password" id="password" type="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:8080/api/login', {
          username: this.username,
          password: this.password
        });
        console.log('Login successful', response.data);
        // Handle login success (store token, redirect, etc.)
      } catch (error) {
        console.error('Login failed', error);
        alert('Login failed!');
      }
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100vh; /* 使容器高度为视口高度 */
  background-color: #f5f5f5; /* 背景色，可以根据需要修改 */
}

.login-form {
  width: 300px; /* 设置表单宽度 */
  padding: 20px; /* 给表单内元素一些间距 */
  border: 1px solid #ccc; /* 边框 */
  border-radius: 5px; /* 边框圆角 */
  background-color: white; /* 表单背景色 */
}

.login-form div {
  margin-bottom: 15px; /* 每个表单项之间的间距 */
}

.login-form label {
  display: block; /* 让标签单独占一行 */
  margin-bottom: 5px; /* 标签与输入框之间的间距 */
}

.login-form input {
  width: 100%; /* 输入框宽度占满整个父容器 */
  padding: 8px; /* 输入框内的间距 */
  border: 1px solid #ccc; /* 输入框边框 */
  border-radius: 4px; /* 输入框圆角 */
}

.login-form button {
  width: 100%; /* 按钮宽度占满整个父容器 */
  padding: 10px; /* 按钮内的间距 */
  background-color: #007bff; /* 按钮背景颜色 */
  color: white; /* 按钮文字颜色 */
  border: none; /* 去除按钮边框 */
  cursor: pointer; /* 鼠标悬停时显示为点击手势 */
  border-radius: 4px; /* 按钮圆角 */
}

.login-form button:hover {
  background-color: #0056b3; /* 按钮悬停时的背景颜色 */
}
</style>
