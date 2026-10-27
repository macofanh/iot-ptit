// Gọi API base URL từ file .env (hoặc cấu hình hardcode nếu chưa fix được env)
const API_BASE_URL = 'http://localhost:8000'

export interface LoginPayload {
    email: string // Ở backend là username
    password: string
}

class AuthService {
    async login(payload: LoginPayload): Promise<{ token: string }> {
        if (!payload.email || !payload.password) {
            throw new Error('Vui lòng nhập đầy đủ thông tin')
        }

        // Backend FastAPI OAuth2PasswordBearer yêu cầu form urlencoded
        const formData = new URLSearchParams()
        formData.append('username', payload.email)
        formData.append('password', payload.password)

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData.toString()
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Sai tài khoản hoặc mật khẩu')
            }

            const data = await response.json()
            const token = data.access_token

            // Lưu Token vào localStorage
            localStorage.setItem('access_token', token)
            
            // Xử lý tạm tên hiển thị: Nếu là admin thì lưu tên của admin
            // (Thực tế backend nên trả về User Profile, ở đây lưu tạm từ tên đăng nhập)
            const fullName = payload.email.toLowerCase() === 'admin' ? 'Đinh Tuấn Anh' : payload.email
            localStorage.setItem('user_full_name', fullName)

            return { token }
        } catch (error: any) {
             throw new Error(error.message || 'Lỗi kết nối đến máy chủ')
        }
    }

    logout() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_full_name')
        window.location.href = '/login' // Đẩy về trang đăng nhập
    }

    isAuthenticated() {
        return !!localStorage.getItem('access_token')
    }
    
    getUserFullName() {
        return localStorage.getItem('user_full_name') || 'Guest'
    }
}

export const authService = new AuthService()