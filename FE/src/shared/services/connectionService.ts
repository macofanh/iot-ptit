import { ref } from 'vue'

/** Fake trạng thái kết nối ESP — dùng chung cho header AppLayout */
export const isEspConnected = ref(false)

export function setEspConnected(connected: boolean) {
    isEspConnected.value = connected
}
