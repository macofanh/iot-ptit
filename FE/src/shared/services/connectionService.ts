import { ref } from 'vue'

/** Fake trạng thái kết nối ESP — dùng chung cho header AppLayout */
export const isEspConnected = ref(false)

// Biến lưu trữ ID của timeout để theo dõi Heartbeat toàn cục
let heartbeatTimeout: number | undefined

export function setEspConnected(connected: boolean) {
    isEspConnected.value = connected

    // Nếu chủ động set OFFLINE (ngắt kết nối), thì xóa luôn bộ đếm
    if (!connected && heartbeatTimeout) {
        clearTimeout(heartbeatTimeout)
    }
}

/**
 * Gọi hàm này mỗi khi nhận được dữ liệu (Heartbeat).
 * Nó sẽ set ONLINE ngay lập tức và tự động set OFFLINE sau 15s nếu không được gọi lại.
 */
export function triggerHeartbeat() {
    isEspConnected.value = true // Chắc chắn đang ONLINE

    if (heartbeatTimeout) {
        clearTimeout(heartbeatTimeout) // Hủy hẹn giờ cũ
    }

    // Cài hẹn giờ mới: 15s sau không ai gọi hàm này nữa thì báo OFFLINE
    heartbeatTimeout = window.setTimeout(() => {
        isEspConnected.value = false
    }, 15000)
}
