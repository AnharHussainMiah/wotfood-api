import { createWebHistory, createRouter } from "vue-router";

import Home from './views/Home.vue'
import Basket from './views/Basket.vue'

const routes = [
    {
        path: '/', component: Home
    },
    {
        path: '/basket', component: Basket
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})