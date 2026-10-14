export interface LoginPayload {
    email: string
    password: string
}

class MockAuthService {
    async login(payload: LoginPayload): Promise<{ token: string }> {
        await new Promise((r) => setTimeout(r, 300))
        if (!payload.email || !payload.password) {
            throw new Error('Vui lòng nhập đầy đủ thông tin')
        }
        const token = 'fake_token_' + Date.now()
        localStorage.setItem('auth_token', token)
        return { token }
    }

    logout() {
        localStorage.removeItem('auth_token')
    }

    isAuthenticated() {
        return !!localStorage.getItem('auth_token')
    }
}

export const authService = new MockAuthService()
