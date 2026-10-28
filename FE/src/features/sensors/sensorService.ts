import type {
    SensorListResult,
    SensorRecord,
    FilterType,
    SortKey,
    SortDir,
} from './sensors'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Định dạng thời gian sang chuẩn Việt Nam: DD/MM/YYYY HH:mm:ss
 * Đồng thời hiểu đúng mốc thời gian UTC từ Backend để khớp với giờ hiện tại (UTC+7)
 */
export function formatDateTime(timeStr: string): string {
    if (!timeStr) return ''
    const str = String(timeStr).trim()

    // 1. Nếu chuỗi ở dạng MM/DD/YYYY hoặc DD/MM/YYYY
    const slashParts = str.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(.*)$/)
    if (slashParts && slashParts[1] && slashParts[2] && slashParts[3]) {
        const p1 = slashParts[1]
        const p2 = slashParts[2]
        const year = slashParts[3]
        const rest = (slashParts[4] || '').replace(/^,\s*/, ' ')
        const n1 = parseInt(p1, 10)
        const n2 = parseInt(p2, 10)
        // Nếu số thứ 2 > 12 -> chắc chắn dạng MM/DD/YYYY (US) -> chuyển sang DD/MM/YYYY
        if (n2 > 12) {
            return `${String(n2).padStart(2, '0')}/${String(n1).padStart(2, '0')}/${year}${rest}`
        }
        // Nếu số thứ 1 > 12 -> chắc chắn đã là DD/MM/YYYY
        if (n1 > 12) {
            return `${String(n1).padStart(2, '0')}/${String(n2).padStart(2, '0')}/${year}${rest}`
        }
    }

    // 2. Chuyển chuỗi thành chuẩn UTC ISO 8601 nếu chưa có ký hiệu timezone (thêm 'Z')
    let s = str
    if (!s.endsWith('Z') && !/[+-]\d{2}:\d{2}$/.test(s)) {
        s = s.replace(' ', 'T').replace(/\//g, '-')
        s = `${s}Z`
    }

    const date = new Date(s)
    if (isNaN(date.getTime())) {
        return str
    }

    // Format sang giờ địa phương của người dùng (UTC+7)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`
}

class SensorService {
    connect() {
        // Lifecycle hook nếu cần kết nối WebSocket/MQTT sau này
    }

    async fetchRecords(params: {
        type?: FilterType
        query?: string
        page?: number
        pageSize?: number
        sortKey?: SortKey | null
        sortDir?: SortDir
    }): Promise<SensorListResult> {
        const page = params.page ?? 1
        const pageSize = params.pageSize ?? 10
        const sortKey = params.sortKey || 'time'
        const sortDir = params.sortDir || 'desc'
        const type = params.type || 'all'

        const queryParams = new URLSearchParams({
            page: String(page),
            pageSize: String(pageSize),
            sortKey: sortKey,
            sortDir: sortDir,
            type: type,
        })

        if (params.query?.trim()) {
            queryParams.append('query', params.query.trim())
        }

        try {
            const token = localStorage.getItem('access_token') || ''
            const response = await fetch(
                `${API_BASE_URL}/api/sensors/history?${queryParams.toString()}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                },
            )

            if (!response.ok) {
                console.error(
                    'Lỗi khi tải dữ liệu cảm biến:',
                    response.status,
                    response.statusText,
                )
                return {
                    items: [],
                    total: 0,
                    page,
                    pageSize,
                }
            }

            const data = await response.json()
            const rawItems: any[] = data.items || []

            // Chuẩn hóa và format lại thời gian theo DD/MM/YYYY HH:mm:ss
            const items: SensorRecord[] = rawItems.map((item) => ({
                id: item.id,
                sensorCode: item.sensorCode,
                type: item.type,
                typeLabel: item.typeLabel,
                value: item.value,
                time: formatDateTime(item.time),
            }))

            return {
                items,
                total: data.total ?? 0,
                page,
                pageSize,
            }
        } catch (error) {
            console.error('Lỗi kết nối tới Backend API:', error)
            return {
                items: [],
                total: 0,
                page,
                pageSize,
            }
        }
    }
}

export const sensorService = new SensorService()
