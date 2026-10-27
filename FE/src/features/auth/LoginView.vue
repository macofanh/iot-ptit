<template>
    <div class="login-wrapper">
        <header class="login-header">
            <div class="brand">
                <span class="material-symbols-outlined brand-icon"
                    >settings_remote</span
                >
                <h1 class="brand-title">IOT PTIT</h1>
            </div>
            <p class="brand-subtitle">
                Chào mừng trở lại. Đăng nhập hệ thống để tiếp tục.
            </p>
        </header>

        <main class="login-card">
            <form @submit.prevent="handleLogin">
                <!-- Email -->
                <div class="field-group">
                    <label class="field-label" for="email">
                        Email hoặc Tên đăng nhập
                    </label>
                    <div
                        class="input-wrapper"
                        :class="{ focused: focusedField === 'email' }"
                    >
                        <span class="material-symbols-outlined input-icon"
                            >mail</span
                        >
                        <input
                            id="email"
                            v-model="email"
                            class="input-field"
                            placeholder="Nhập tài khoản (VD: admin)"
                            required
                            type="text"
                            @focus="focusedField = 'email'"
                            @blur="focusedField = ''"
                        />
                    </div>
                </div>

                <!-- Mật khẩu -->
                <div class="field-group">
                    <div class="field-label-row">
                        <label class="field-label" for="password"
                            >Mật khẩu</label
                        >
                        <a class="forgot-link" href="#">Quên mật khẩu?</a>
                    </div>
                    <div
                        class="input-wrapper"
                        :class="{ focused: focusedField === 'password' }"
                    >
                        <span class="material-symbols-outlined input-icon"
                            >lock</span
                        >
                        <input
                            id="password"
                            v-model="password"
                            class="input-field"
                            placeholder="Nhập mật khẩu"
                            required
                            :type="showPassword ? 'text' : 'password'"
                            @focus="focusedField = 'password'"
                            @blur="focusedField = ''"
                        />
                        <button
                            aria-label="Toggle password visibility"
                            class="toggle-pw-btn"
                            type="button"
                            @click="showPassword = !showPassword"
                        >
                            <span class="material-symbols-outlined">{{
                                showPassword ? 'visibility_off' : 'visibility'
                            }}</span>
                        </button>
                    </div>
                </div>

                <!-- Lỗi -->
                <p v-if="error" class="error-msg">{{ error }}</p>

                <!-- Submit -->
                <button class="submit-btn" type="submit" :disabled="loading">
                    <span v-if="loading" class="material-symbols-outlined spin"
                        >progress_activity</span
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
const focusedField = ref('')

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        await authService.login({
            email: email.value,
            password: password.value,
        })
        router.push({ path: '/home' })
    } catch (e) {
        error.value = e instanceof Error ? e.message : 'Đăng nhập thất bại'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
/* ── Wrapper ── */
.login-wrapper {
    min-height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    padding: 1.5rem;
    margin-top: 15rem;
    box-sizing: border-box;
}

/* ── Header / Brand ── */
.login-header {
    width: 100%;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 2rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #4f46e5;
    margin-bottom: 0.75rem;
}

.brand-icon {
    font-size: 2.5rem;
}

.brand-title {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0;
    color: #4f46e5;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
}

.brand-subtitle {
    font-size: 0.9375rem;
    color: #6b7280;
    text-align: center;
    margin: 0;
    line-height: 1.5;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
}

/* ── Card ── */
.login-card {
    width: 100%;
    max-width: 440px;
    background: #ffffff;
    border-radius: 0.75rem;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    box-sizing: border-box;
}

/* ── Form ── */
form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

/* ── Field ── */
.field-group {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
}

.field-label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.field-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
}

.forgot-link {
    font-size: 0.8125rem;
    font-weight: 500;
    color: #4f46e5;
    text-decoration: none;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
}

.forgot-link:hover {
    text-decoration: underline;
}

/* ── Input wrapper ── */
.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    transition:
        box-shadow 0.15s ease,
        border-color 0.15s ease;
}

.input-wrapper.focused {
    border-color: #4f46e5;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
}

.input-icon {
    position: absolute;
    left: 0.75rem;
    color: #9ca3af;
    font-size: 1.25rem;
    pointer-events: none;
    user-select: none;
}

.input-field {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    padding: 0.625rem 2.75rem 0.625rem 2.5rem;
    font-size: 0.875rem;
    color: #1f2937;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
    box-sizing: border-box;
}

.input-field::placeholder {
    color: #9ca3af;
}

/* ── Toggle password button ── */
.toggle-pw-btn {
    position: absolute;
    right: 0.75rem;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    color: #9ca3af;
    transition: color 0.15s;
}

.toggle-pw-btn:hover {
    color: #4b5563;
}

.toggle-pw-btn .material-symbols-outlined {
    font-size: 1.25rem;
}

/* ── Error ── */
.error-msg {
    font-size: 0.875rem;
    font-weight: 500;
    color: #ef4444;
    margin: -0.25rem 0 0;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
}

/* ── Submit button ── */
.submit-btn {
    width: 100%;
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 0.5rem;
    padding: 0.8125rem 1rem;
    font-size: 0.9375rem;
    font-weight: 600;
    font-family:
        system-ui,
        -apple-system,
        sans-serif;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    transition:
        background-color 0.15s ease,
        transform 0.1s ease;
    margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
    background-color: #4338ca;
}

.submit-btn:active:not(:disabled) {
    transform: scale(0.98);
}

.submit-btn:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

/* ── Spinner ── */
.spin {
    font-size: 1.25rem;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

/* ── Responsive ── */
@media (max-width: 480px) {
    .login-card {
        padding: 1.5rem;
    }
}
</style>
