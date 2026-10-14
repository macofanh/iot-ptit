import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/features/auth/LoginView.vue'),
    },
    {
        path: '/',
        component: () =>
            import('@/shared/layout/AppLayout.vue'),
        children: [
            {
                path: '',
                redirect: '/home',
            },
            {
                path: 'home',
                name: 'Home',
                component: () => import('@/features/home/HomeView.vue'),
            },
            {
                path: 'sensors',
                name: 'Sensors',
                component: () =>
                    import('@/features/sensors/SensorDataView.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () =>
                    import('@/features/history/ActionLogView.vue'),
            },
            {
                path: 'profile',
                name: 'Profile',
                component: () =>
                    import('@/features/profile/ProfileView.vue'),
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
