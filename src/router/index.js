import { createRouter, createWebHistory } from 'vue-router'; // 使用命名导入
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Upload from "@/views/Upload.vue";
import SentimentAnalysisChart from "@/views/SentimentAnalysisChart.vue";


const routes = [
    {
        path: '/',
        redirect: '/login'  // 默认重定向到登录页面
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },{
        path: '/upload',
        name: 'Upload',
        component: Upload
    },{
        path: '/sentiment-analysis',
        name: 'sentiment-analysis',
        component: SentimentAnalysisChart,
    }

];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;  // 继续使用 export default
