<template>
    <div
        class="font-body-md text-on-surface bg-[#F8F9FA] flex min-h-screen relative overflow-x-hidden"
    >
        <aside
            id="navDrawer"
            class="fixed inset-y-0 left-0 z-50 flex flex-col p-md shadow-md h-full w-72 rounded-r-xl transition-transform duration-300 transform -translate-x-full md:translate-x-0"
            :class="{ 'translate-x-0': sidebarOpen }"
        >
            <div class="flex items-center gap-sm mb-lg px-xs">
                <h1
                    class="font-headline-lg text-headline-lg text-primary dark:text-primary-fixed-dim font-bold tracking-tight"
                >
                    IoT Monitor
                </h1>
            </div>
            <nav class="flex flex-col gap-sm flex-1">
                <RouterLink
                    v-for="item in navItems"
                    :key="item.to"
                    :to="item.to"
                    class="flex items-center gap-md px-md py-sm rounded-lg font-label-md text-[13px] font-medium transition-colors duration-200 active:scale-[0.98]"
                    :class="
                        isActive(item.to)
                            ? 'bg-primary-container text-on-primary-container'
                            : 'text-on-surface-variant hover:bg-surface-variant'
                    "
                    @click="closeSidebarOnMobile"
                >
                    <span
                        class="material-symbols-outlined text-[26px]"
                        :class="{ 'icon-fill': isActive(item.to) }"
                        >{{ item.icon }}</span
                    >
                    {{ item.label }}
                </RouterLink>
            </nav>
        </aside>

        <div
            v-if="sidebarOpen"
            class="fixed inset-0 bg-black/30 z-40 md:hidden"
            @click="sidebarOpen = false"
        />

        <main
            class="flex-1 flex flex-col md:ml-72 w-full transition-all duration-300 min-h-screen"
        >
            <header
                class="sticky top-0 w-full z-40 flex justify-between items-center px-margin-mobile h-16 bg-surface-container-lowest dark:bg-surface-dim shadow-sm"
            >
                <div class="flex items-center gap-sm">
                    <button
                        type="button"
                        class="md:hidden text-primary hover:bg-surface-container-high rounded-full p-sm active:scale-95"
                        @click="sidebarOpen = !sidebarOpen"
                    >
                        <span class="material-symbols-outlined">menu</span>
                    </button>
                    <h2
                        class="font-headline-sm text-headline-sm font-bold text-primary md:hidden"
                    >
                        IoT Monitor
                    </h2>
                    <h2
                        class="font-headline-sm text-headline-sm font-bold text-on-surface hidden md:block"
                    >
                        Trạng Thái Kết Nối ESP:
                        <span
                            class="font-bold"
                            :class="
                                isEspConnected
                                    ? 'text-emerald-600'
                                    : 'text-error'
                            "
                        >
                            {{ isEspConnected ? 'ONLINE' : 'OFFLINE' }}
                        </span>
                    </h2>
                </div>
                
                <!-- Hiển thị tên động và Nút đăng xuất -->
                <div class="flex items-center gap-sm cursor-pointer hover:bg-gray-100 p-2 rounded-lg transition-colors" @click="handleLogout" title="Đăng xuất">
                    <span class="font-medium text-body-md text-on-surface hidden sm:block">
                        {{ userName }}
                    </span>
                    <div
                        class="w-10 h-10 rounded-full bg-primary-fixed flex items-center justify-center text-primary font-bold shadow-sm"
                    >
                        <span class="material-symbols-outlined text-[20px]">person</span>
                    </div>
                </div>
            </header>

            <router-view />
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { isEspConnected } from '@/shared/services/connectionService'
import { authService } from '@/features/auth/authService' // Điều chỉnh lại đường dẫn nếu file nằm chỗ khác

const route = useRoute()
const sidebarOpen = ref(false)
const userName = ref('')

const navItems = [
    { to: '/home', label: 'Trang Chủ', icon: 'home' },
    { to: '/sensors', label: 'Dữ liệu cảm biến', icon: 'database' },
    { to: '/history', label: 'Lịch sử thao tác', icon: 'history' },
    { to: '/profile', label: 'Hồ sơ', icon: 'person' },
]

const isActive = (path: string) =>
    route.path === path || route.path.startsWith(path + '/')

const closeSidebarOnMobile = () => {
    if (window.innerWidth < 768) sidebarOpen.value = false
}

const handleLogout = () => {
    if(confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        authService.logout()
    }
}

onMounted(() => {
    userName.value = authService.getUserFullName()
})
</script>

<style scoped>
.icon-fill {
    font-variation-settings: 'FILL' 1;
}
</style>