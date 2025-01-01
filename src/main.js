import { createApp } from 'vue';  // 使用 Vue 3 的导入方式
import App from './App.vue';
import router from './router';  // 导入路由实例

const app = createApp(App);

app.use(router);  // 使用 Vue Router

app.mount('#app');
