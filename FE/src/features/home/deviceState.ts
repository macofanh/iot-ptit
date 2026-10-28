import { reactive } from 'vue'

export type DeviceId = 'led1' | 'led2' | 'all'

// Module-level => tồn tại suốt vòng đời app, không bị reset khi đổi trang
export const devices = reactive({
    led1: false,
    led2: false,
    all: false,
    air: false,
})

export function applyDeviceStatus(device: string, isOn: boolean) {
    if (device === 'led1') devices.led1 = isOn
    else if (device === 'led2') devices.led2 = isOn
    else if (device === 'all') {
        devices.led1 = isOn
        devices.led2 = isOn
    }
    // Tự động đồng bộ "Tất Cả Đèn"
    devices.all = devices.led1 && devices.led2
}