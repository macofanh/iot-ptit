import type { SensorData, StatusResponse } from './home'
import { triggerHeartbeat, setEspConnected } from '@/shared/services/connectionService'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Ngưỡng: nếu bản ghi nhận được trong vòng 15 giây → coi là ONLINE
const OFFLINE_THRESHOLD_MS = 15000

class MqttService {
    private timer: number | null = null
    private onStatusChangeCallback: ((status: StatusResponse) => void) | null = null

    public connect(
        _brokerUrl: string,
        _options: any,
        onSensorData: (data: SensorData) => void,
        onStatusChange: (status: StatusResponse) => void,
        _onConnectionChange: (connected: boolean) => void,
    ) {
        this.onStatusChangeCallback = onStatusChange
        this.fetchLatestSensorData(onSensorData)
        this.timer = window.setInterval(() => {
            this.fetchLatestSensorData(onSensorData)
        }, 5000)
    }

    private async fetchLatestSensorData(onSensorData: (data: SensorData) => void) {
        try {
            const token = localStorage.getItem('access_token') || ''
            const response = await fetch(`${API_BASE_URL}/api/sensors/latest`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
            })

            if (response.ok) {
                const result = await response.json()

                if (result.data) {
                    // 1. Luôn cập nhật số liệu cảm biến mới nhất lên giao diện
                    onSensorData({
                        temperature: result.data.temperature,
                        humidity: result.data.humidity,
                        light: result.data.light,
                    })

                    // 2. Thêm 'Z' để JavaScript hiểu đúng giờ UTC từ Backend (tránh lệch 7 tiếng)
                    const rawCreatedAt = String(result.data.created_at)
                    const dateStr = rawCreatedAt.endsWith('Z')
                        ? rawCreatedAt
                        : `${rawCreatedAt}Z`
                    const recordTime = new Date(dateStr).getTime()
                    const now = Date.now()
                    const ageMs = now - recordTime

                    // 3. Nếu bản ghi mới trong vòng 15s -> ESP32 đang ONLINE
                    if (ageMs <= OFFLINE_THRESHOLD_MS && ageMs >= -10000) {
                        triggerHeartbeat()
                    } else {
                        console.warn(`Dữ liệu cũ ${Math.round(ageMs / 1000)}s — ESP32 đang OFFLINE`)
                        setEspConnected(false)
                    }
                } else {
                    setEspConnected(false)
                }
            } else {
                console.warn('Lỗi từ API Server:', response.status)
                if (response.status === 401) {
                    console.warn('Token hết hạn hoặc chưa đăng nhập')
                }
                setEspConnected(false)
            }
        } catch (error) {
            console.error('Không thể kết nối đến Backend API:', error)
            setEspConnected(false)
        }
    }

    public async publishControl(topic: string, command: '1' | '0'): Promise<boolean> {
        const deviceMap: Record<string, { id: number; name: string; endpoint: string }> = {
            'iot/control/led1': { id: 1, name: 'led1', endpoint: `${API_BASE_URL}/api/devices/1/control` },
            'iot/control/led2': { id: 2, name: 'led2', endpoint: `${API_BASE_URL}/api/devices/2/control` },
            'iot/control/all': { id: 0, name: 'all', endpoint: `${API_BASE_URL}/api/devices/all/control` },
        }

        const target = deviceMap[topic]
        if (!target) return false

        try {
            const token = localStorage.getItem('access_token') || ''
            const response = await fetch(target.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ action: command }),
            })

            if (response.ok) {
                const resData = await response.json()
                if (resData.success) {
                    if (this.onStatusChangeCallback) {
                        this.onStatusChangeCallback({
                            device: target.name,
                            status: command,
                            action: 'success',
                        })
                    }
                    return true
                } else {
                    console.warn('ESP32 không phản hồi hoặc timeout:', resData.message)
                    return false
                }
            } else {
                console.warn('Lỗi khi điều khiển thiết bị:', response.status)
                return false
            }
        } catch (error) {
            console.error('Lỗi kết nối điều khiển thiết bị:', error)
            return false
        }
    }

    public disconnect() {
        if (this.timer) {
            clearInterval(this.timer)
            this.timer = null
        }
    }
}

export const mqttService = new MqttService()