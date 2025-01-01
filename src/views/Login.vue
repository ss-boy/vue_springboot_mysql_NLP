<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
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
      <div class="register-link">
        <p>Don't have an account?</p>
        <button @click="goToRegister">Register</button>
      </div>
    </div>
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
        this.$router.push('/Upload');
      } catch (error) {
        console.error('Login failed', error);
        alert('Login failed!');
      }
    },
    goToRegister() {
      // 使用 Vue Router 跳转到注册页面
      this.$router.push('/register');
    }
  }
};
</script>

<style scoped>
/* 设置背景图片 */
.login-container {
  height: 100vh;
  background-image: url('@/assets/image/bg.jpg'); /* 图片路径 */
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-form {
  background-color: rgba(255, 255, 255, 0.8); /* 背景色带透明度 */
  padding: 30px;
  border-radius: 10px;
  width: 400px; /* 可以根据需要调整宽度 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  font-size: 24px;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: blue;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: darkblue;
}

.register-link {
  margin-top: 20px;
  text-align: center;
}

.register-link p {
  margin: 0;
}

.register-link button {
  background-color: transparent;
  color: blue;
  border: none;
  text-decoration: underline;
  cursor: pointer;
}

.register-link button:hover {
  color: darkblue;
}
</style>
