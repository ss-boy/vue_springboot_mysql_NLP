<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input v-model="email" id="email" type="email" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input v-model="password" id="password" type="password" required />
      </div>
      <div>
        <label for="confirmPassword">Confirm Password</label>
        <input v-model="confirmPassword" id="confirmPassword" type="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }
      try {
        const response = await axios.post('http://localhost:8080/api/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        console.log('Registration successful', response.data);
        // Handle registration success (redirect to login page, etc.)
      } catch (error) {
        console.error('Registration failed', error);
        alert('Registration failed!');
      }
    }
  }
};
</script>

<style scoped>
/* Add your styling here */
</style>
