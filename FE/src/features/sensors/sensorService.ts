import type {
    SensorListResult,
    SensorRecord,
    SensorType,
    SortKey,
    SortDir,
} from './sensors'

const FAKE_ROWS: SensorRecord[] = [
    {
        id: 32,
        sensorCode: '#LIGHT-01',
        type: 'light',
        typeLabel: 'Ánh sáng',
        value: '800 lux',
        time: '2026/10/07 16:30:15',
    },
    {
        id: 33,
        sensorCode: '#HUMI-01',
        type: 'humidity',
        typeLabel: 'Độ ẩm',
        value: '50.9 %',
        time: '2026/10/07 16:30:15',
    },
    {
        id: 34,
        sensorCode: '#TEMP-01',
        type: 'temperature',
        typeLabel: 'Nhiệt độ',
        value: '25.6 °C',
        time: '2026/10/07 16:30:15',
    },
    {
        id: 35,
        sensorCode: '#LIGHT-01',
        type: 'light',
        typeLabel: 'Ánh sáng',
        value: '783 lux',
        time: '2026/10/07 16:30:13',
    },
    {
        id: 36,
        sensorCode: '#HUMI-01',
        type: 'humidity',
        typeLabel: 'Độ ẩm',
        value: '51.1 %',
        time: '2026/10/07 16:30:13',
    },
    {
        id: 37,
        sensorCode: '#TEMP-01',
        type: 'temperature',
        typeLabel: 'Nhiệt độ',
        value: '25.6 °C',
        time: '2026/10/07 16:30:13',
    },
    {
        id: 38,
        sensorCode: '#LIGHT-01',
        type: 'light',
        typeLabel: 'Ánh sáng',
        value: '740 lux',
        time: '2026/10/07 16:30:11',
    },
    {
        id: 39,
        sensorCode: '#HUMI-01',
        type: 'humidity',
        typeLabel: 'Độ ẩm',
        value: '51.2 %',
        time: '2026/10/07 16:30:11',
    },
    {
        id: 40,
        sensorCode: '#TEMP-01',
        type: 'temperature',
        typeLabel: 'Nhiệt độ',
        value: '25.6 °C',
        time: '2026/10/07 16:30:11',
    },
    {
        id: 41,
        sensorCode: '#LIGHT-01',
        type: 'light',
        typeLabel: 'Ánh sáng',
        value: '741 lux',
        time: '2026/10/07 16:30:09',
    },
]

class MockSensorService {
    connect() {}

    async fetchRecords(params: {
        type?: SensorType | 'all'
        query?: string
        page?: number
        pageSize?: number
        sortKey?: SortKey | null
        sortDir?: SortDir
    }): Promise<SensorListResult> {
        await new Promise((r) => setTimeout(r, 150))

        let items = [...FAKE_ROWS]
        if (params.type && params.type !== 'all') {
            items = items.filter((r) => r.type === params.type)
        }
        if (params.query?.trim()) {
            const q = params.query.trim().toLowerCase()
            items = items.filter(
                (r) =>
                    r.sensorCode.toLowerCase().includes(q) ||
                    r.value.toLowerCase().includes(q) ||
                    r.time.toLowerCase().includes(q) ||
                    String(r.id).includes(q),
            )
        }

        if (params.sortKey) {
            const key = params.sortKey
            const dir = params.sortDir === 'desc' ? -1 : 1
            items.sort((a, b) => {
                if (key === 'id') return (a.id - b.id) * dir
                if (key === 'value') {
                    // "800 lux", "50.9 %", "25.6 °C" -> lấy phần số
                    return (parseFloat(a.value) - parseFloat(b.value)) * dir
                }
                // time dạng yyyy/MM/dd HH:mm:ss nên so sánh chuỗi là đúng
                return String(a[key]).localeCompare(String(b[key]), 'vi') * dir
            })
        }

        const page = params.page ?? 1
        const pageSize = params.pageSize ?? 10
        return {
            items,
            total: 1000,
            page,
            pageSize,
        }
    }
}

export const sensorService = new MockSensorService()
