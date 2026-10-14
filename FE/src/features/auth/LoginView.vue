<template>
    <div
        class="bg-background text-on-background min-h-screen flex flex-col justify-center items-center p-margin-mobile"
    >
        <header class="w-full max-w-md flex flex-col items-center mb-xl">
            <div
                class="flex items-center justify-center gap-sm text-primary mb-sm"
            >
                <span
                    class="material-symbols-outlined text-data-display"
                    >settings_remote</span
                >
                <h1 class="font-headline-lg text-headline-lg">Lumina IoT</h1>
            </div>
            <p
                class="font-body-md text-body-md text-on-surface-variant text-center"
            >
                Chào mừng trở lại. Đăng nhập hệ thống để tiếp tục.
            </p>
        </header>

        <main
            class="w-full max-w-md bg-surface-container-lowest rounded-xl shadow-[0px_4px_20px_rgba(0,0,0,0.04)] p-lg flex flex-col gap-lg"
        >
            <form class="flex flex-col gap-md" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-xs">
                    <label
                        class="font-label-md text-label-md text-on-surface"
                        for="email"
                        >Email hoặc Tên đăng nhập</label
                    >
                    <div
                        class="relative flex items-center bg-surface-container-low rounded-lg focus-within:ring-2 focus-within:ring-primary transition-shadow"
                    >
                        <span
                            class="material-symbols-outlined absolute left-md text-outline"
                            >mail</span
                        >
                        <input
                            id="email"
                            v-model="email"
                            class="w-full bg-transparent border-none pl-xl pr-md py-sm font-body-md text-body-md text-on-surface focus:ring-0 placeholder:text-outline-variant"
                            placeholder="Nhập email của bạn"
                            required
                            type="text"
                        />
                    </div>
                </div>

                <div class="flex flex-col gap-xs">
                    <div class="flex justify-between items-center">
                        <label
                            class="font-label-md text-label-md text-on-surface"
                            for="password"
                            >Mật khẩu</label
                        >
                        <a
                            class="font-label-md text-label-md text-primary hover:underline transition-all"
                            href="#"
                            >Quên mật khẩu?</a
                        >
                    </div>
                    <div
                        class="relative flex items-center bg-surface-container-low rounded-lg focus-within:ring-2 focus-within:ring-primary transition-shadow"
                    >
                        <span
                            class="material-symbols-outlined absolute left-md text-outline"
                            >lock</span
                        >
                        <input
                            id="password"
                            v-model="password"
                            class="w-full bg-transparent border-none pl-xl pr-xl py-sm font-body-md text-body-md text-on-surface focus:ring-0 placeholder:text-outline-variant"
                            placeholder="Nhập mật khẩu"
                            required
                            :type="showPassword ? 'text' : 'password'"
                        />
                        <button
                            aria-label="Toggle password visibility"
                            class="absolute right-md text-outline hover:text-on-surface transition-colors focus:outline-none"
                            type="button"
                            @click="showPassword = !showPassword"
                        >
                            <span class="material-symbols-outlined">{{
                                showPassword ? 'visibility_off' : 'visibility'
                            }}</span>
                        </button>
                    </div>
                </div>

                <p v-if="error" class="text-error text-label-md">{{ error }}</p>

                <button
                    class="mt-sm w-full bg-primary-container text-on-primary-container font-headline-sm text-headline-sm rounded-lg py-md flex justify-center items-center hover:opacity-90 active:scale-[0.98] transition-all duration-150 shadow-[0_4px_10px_rgba(109,40,217,0.2)]"
                    type="submit"
                    :disabled="loading"
                >
                    {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
                </button>
            </form>
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from './authService'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        await authService.login({
            email: email.value,
            password: password.value,
        })
        router.push({ name: 'Home' })
    } catch (e) {
        error.value = e instanceof Error ? e.message : 'Đăng nhập thất bại'
    } finally {
        loading.value = false
    }
}
</script>
