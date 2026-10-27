<template>
    <div
        class="p-margin-mobile md:p-lg lg:p-xl max-w-7xl mx-auto w-full flex flex-col gap-lg h-[calc(100vh-4rem)] overflow-hidden relative"
    >
        <!-- Toast thông báo nhỏ -->
        <Transition name="toast">
            <div
                v-if="toastMessage"
                class="fixed top-20 right-6 z-50 flex items-center gap-2.5 px-4 py-3 rounded-xl shadow-lg border text-sm font-medium backdrop-blur-md transition-all duration-300"
                :class="
                    toastType === 'error'
                        ? 'bg-red-50/95 text-red-700 border-red-200 shadow-red-500/10'
                        : 'bg-emerald-50/95 text-emerald-700 border-emerald-200 shadow-emerald-500/10'
                "
            >
                <span class="material-symbols-outlined text-[20px] flex-shrink-0">
                    {{ toastType === 'error' ? 'error' : 'check_circle' }}
                </span>
                <span>{{ toastMessage }}</span>
            </div>
        </Transition>

        <!-- 1. Cụm Card thông số cảm biến -->
        <section class="grid grid-cols-1 sm:grid-cols-3 gap-md flex-shrink-0">
            <SensorCard
                title="Ánh sáng"
                :value="sensorData.light"
                unit="lux"
                icon="light_mode"
                iconColorClass="text-secondary-fixed-dim"
                badgeBgClass="bg-secondary-fixed-dim"
            />
            <SensorCard
                title="Nhiệt độ"
                :value="sensorData.temperature"
                unit="°C"
                icon="device_thermostat"
                iconColorClass="text-tertiary-container"
                badgeBgClass="bg-tertiary-container"
                :decimals="2"
            />
            <SensorCard
                title="Độ ẩm"
                :value="sensorData.humidity"
                unit="%"
                icon="water_drop"
                iconColorClass="text-[#3b82f6]"
                badgeBgClass="bg-[#3b82f6]"
            />
        </section>

        <!-- 2. Khung Bố cục chính (Biểu đồ bên Trái, Control bên Phải) -->
        <div
            class="grid grid-cols-1 lg:grid-cols-3 gap-md flex-1 min-h-0 items-start"
        >
            <!-- CỘT TRÁI (2/3): Biểu đồ giám sát thời gian thực -->
            <section
                class="lg:col-span-2 bg-surface-container-lowest rounded-xl p-md ambient-shadow flex flex-col gap-sm h-full min-h-0"
            >
                <div
                    class="flex items-center justify-between flex-shrink-0 border-b border-gray-100 pb-3"
                >
                    <h3
                        class="font-headline-sm text-headline-sm text-on-surface font-semibold"
                    >
                        Biểu đồ giám sát thời gian thực
                    </h3>

                    <!-- Lọc biểu đồ -->
                    <div class="flex items-center gap-2">
                        <label class="text-[12px] text-gray-500 font-medium"
                            >Lọc biểu đồ:</label
                        >
                        <select
                            v-model="chartFilter"
                            class="bg-[#F1F5F9] border border-[#E2E8F0] text-gray-700 text-[12px] rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer font-medium"
                        >
                            <option value="all">Tất cả chỉ số</option>
                            <option value="temp">Chỉ Nhiệt độ</option>
                            <option value="humidity">Chỉ Độ ẩm</option>
                            <option value="light">Chỉ Ánh sáng</option>
                        </select>
                    </div>
                </div>

                <!-- Component Biểu đồ Gộp (Nhận mảng dữ liệu lịch sử) -->
                <div class="flex-1 min-h-0">
                    <CombinedChart
                        :data="chartHistory"
                        :filter="chartFilter"
                        @update:filter="chartFilter = $event"
                    />
                </div>
            </section>

            <!-- CỘT PHẢI (1/3): Điều khiển thiết bị ngoại vi -->
            <section
                class="lg:col-span-1 bg-surface-container-lowest rounded-xl p-md ambient-shadow flex flex-col gap-sm h-full min-h-0"
            >
                <h3
                    class="font-headline-sm text-headline-sm text-on-surface font-semibold flex-shrink-0 border-b border-gray-100 pb-3"
                >
                    Điều khiển thiết bị ngoại vi
                </h3>

                <!-- Danh sách nút bấm -->
                <div class="flex flex-col gap-3 mt-1">
                    <DeviceControl
                        name="Đèn Vàng"
                        :status="devices.led1"
                        :loading="loadingDevices.led1"
                        icon="lightbulb"
                        activeBgClass="bg-amber-100"
                        activeIconClass="text-amber-600"
                        @toggle="handleToggle('led1', 'iot/control/led1')"
                    />
                    <DeviceControl
                        name="Đèn Đỏ"
                        :status="devices.led2"
                        :loading="loadingDevices.led2"
                        icon="lightbulb"
                        activeBgClass="bg-red-100"
                        activeIconClass="text-red-600"
                        @toggle="handleToggle('led2', 'iot/control/led2')"
                    />
                    <DeviceControl
                        name="Tất Cả Đèn"
                        :status="devices.all"
                        :loading="loadingDevices.all"
                        icon="power_settings_new"
                        activeBgClass="bg-purple-100"
                        activeIconClass="text-purple-600"
                        @toggle="handleToggle('all', 'iot/control/all')"
                    />
                </div>
            </section>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import SensorCard from './components/SensorCard.vue'
import DeviceControl from './components/DeviceControl.vue'
import CombinedChart from './components/CombinedChart.vue'
import { mqttService } from './mqttService'
import type { SensorData, StatusResponse } from './home'
import { isEspConnected, setEspConnected } from '@/shared/services/connectionService'

const chartFilter = ref('all')

const sensorData = reactive<SensorData>({
    temperature: 0,
    humidity: 0,
    light: 0,
})

// Mảng lưu trữ dữ liệu lịch sử để vẽ biểu đồ (Lưu tối đa 6-8 điểm)
const chartHistory = ref<
    { time: string; temp: number; hum: number; light: number }[]
>([])

const devices = reactive({
    led1: false,
    led2: false,
    all: false,
    air: false,
})

// Trạng thái loading cho từng thiết bị khi đang gửi lệnh
const loadingDevices = reactive({
    led1: false,
    led2: false,
    all: false,
})

// Quản lý Toast thông báo nhỏ
const toastMessage = ref('')
const toastType = ref<'error' | 'success'>('error')
let toastTimeout: number | undefined

const showToast = (message: string, type: 'error' | 'success' = 'error') => {
    toastMessage.value = message
    toastType.value = type
    if (toastTimeout) clearTimeout(toastTimeout)
    toastTimeout = window.setTimeout(() => {
        toastMessage.value = ''
    }, 3000)
}

const handleToggle = async (deviceId: 'led1' | 'led2' | 'all', topic: string) => {
    // Yêu cầu 2: Nếu không có kết nối (OFFLINE) -> Hiển thị thông báo nhỏ, không cho bật/tắt
    if (!isEspConnected.value) {
        showToast('Không thể bật/tắt thiết bị khi ESP32 đang OFFLINE!', 'error')
        return
    }

    // Tránh bấm liên tục khi lệnh trước đang xử lý
    if (loadingDevices[deviceId]) return

    // Yêu cầu 1: Bật hiệu ứng loading trong thời gian chờ phản hồi từ thiết bị
    loadingDevices[deviceId] = true
    if (deviceId === 'all') {
        loadingDevices.led1 = true
        loadingDevices.led2 = true
    }

    const targetState = !devices[deviceId]
    const command = targetState ? '1' : '0'

    try {
        const success = await mqttService.publishControl(topic, command)
        if (success) {
            showToast(
                `Đã ${targetState ? 'bật' : 'tắt'} ${
                    deviceId === 'all'
                        ? 'tất cả đèn'
                        : deviceId === 'led1'
                          ? 'Đèn Vàng'
                          : 'Đèn Đỏ'
                } thành công!`,
                'success',
            )
        } else {
            showToast('Thiết bị không phản hồi hoặc đã quá thời gian chờ (timeout)!', 'error')
        }
    } catch {
        showToast('Lỗi gửi lệnh điều khiển đến máy chủ!', 'error')
    } finally {
        loadingDevices[deviceId] = false
        if (deviceId === 'all') {
            loadingDevices.led1 = false
            loadingDevices.led2 = false
        }
    }
}

onMounted(() => {
    mqttService.connect(
        'ws://172.20.10.2:9001',
        {
            username: 'DTA',
            password: 'B23DCCN014',
            clientId: `vue_client_${Math.random().toString(16).substring(2, 8)}`,
        },
        (newSensorData: SensorData) => {
            Object.assign(sensorData, newSensorData)

            // Xử lý thời gian hiện tại
            const now = new Date()
            const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`

            // Đẩy dữ liệu mới vào mảng đồ thị
            chartHistory.value.push({
                time: timeStr,
                temp: newSensorData.temperature,
                hum: newSensorData.humidity,
                light: newSensorData.light,
            })

            // Giữ lại tối đa 7 mốc thời gian gần nhất trên đồ thị
            if (chartHistory.value.length > 7) {
                chartHistory.value.shift()
            }
        },
        (statusResp: StatusResponse) => {
            if (statusResp.action === 'success') {
                const isOn = statusResp.status === '1'
                if (statusResp.device === 'led1') devices.led1 = isOn
                else if (statusResp.device === 'led2') devices.led2 = isOn
                else if (statusResp.device === 'all') {
                    devices.all = isOn
                    devices.led1 = isOn
                    devices.led2 = isOn
                }
                // Tự động đồng bộ trạng thái "Tất Cả Đèn"
                devices.all = devices.led1 && devices.led2
            }
        },
        (connected: boolean) => {
            setEspConnected(connected)
        },
    )
})

onUnmounted(() => {
    mqttService.disconnect()
    if (toastTimeout) clearTimeout(toastTimeout)
})
</script>

<style scoped>
/* Hiệu ứng Toast animation */
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-enter-from {
    opacity: 0;
    transform: translateY(-12px) scale(0.95);
}
.toast-leave-to {
    opacity: 0;
    transform: translateY(-8px) scale(0.95);
}
</style>
