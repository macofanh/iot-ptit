import type { SensorData, StatusResponse } from './home'

class MockMqttService {
    private timer: number | null = null
    private onStatusChangeCallback: ((status: StatusResponse) => void) | null =
        null

    public connect(
        _brokerUrl: string,
        _options: any,
        onSensorData: (data: SensorData) => void,
        onStatusChange: (status: StatusResponse) => void,
        onConnectionChange: (connected: boolean) => void,
    ) {
        // 1. Giả lập kết nối thành công -> Màn hình hiển thị ONLINE
        onConnectionChange(false)

        // Lưu lại callback để phản hồi khi nhấn nút toggle
        this.onStatusChangeCallback = onStatusChange

        // 2. Set dữ liệu ban đầu
        onSensorData({
            temperature: 26.5,
            humidity: 62,
            light: 850,
        })

        // 3. Giả lập cảm biến gửi dữ liệu nhảy số tự động mỗi 5 giây
        this.timer = window.setInterval(() => {
            const fakeSensorData: SensorData = {
                temperature: Number((24 + Math.random() * 5).toFixed(1)), // Từ 24.0 đến 29.0 °C
                humidity: Math.floor(55 + Math.random() * 20), // Từ 55% đến 75%
                light: Math.floor(500 + Math.random() * 400), // Từ 500 đến 900 lux
            }
            onSensorData(fakeSensorData)
        }, 5000)
    }

    public publishControl(topic: string, command: '1' | '0') {
        const deviceMap: Record<string, string> = {
            'iot/control/led1': 'led1',
            'iot/control/led2': 'led2',
            'iot/control/all': 'all',
            'iot/control/airConditioner': 'air'
        }

        const device = deviceMap[topic] || 'led1'

        // 4. Giả lập ESP32 nhận lệnh và phản hồi "success" sau 200ms
        setTimeout(() => {
            if (this.onStatusChangeCallback) {
                this.onStatusChangeCallback({
                    device,
                    status: command,
                    action: 'success',
                })
            }
        }, 200)
    }

    public disconnect() {
        if (this.timer) {
            clearInterval(this.timer)
            this.timer = null
        }
    }
}

export const mqttService = new MockMqttService()
