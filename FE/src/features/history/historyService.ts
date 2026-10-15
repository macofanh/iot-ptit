import type {
    ActionLog,
    ActionLogResult,
    SortKey,
    SortDir,
    HistoryFilters,
} from './history'

const FAKE_LOGS: ActionLog[] = [
    {
        id: 1,
        device: 'Đèn 1',
        action: 'on',
        actionLabel: 'Bật',
        status: 'success',
        statusLabel: 'Thành công',
        user: 'Admin',
        time: '2026/10/24 10:45:12',
    },
    {
        id: 2,
        device: 'Đèn 2',
        action: 'off',
        actionLabel: 'Tắt',
        status: 'failed',
        statusLabel: 'Thất bại',
        user: 'Lê Thị B',
        time: '2026/10/24 09:30:40',
    },
    {
        id: 3,
        device: 'Quạt thông gió',
        action: 'on',
        actionLabel: 'Bật',
        status: 'pending',
        statusLabel: 'Đang chờ',
        user: 'Mac',
        time: '2026/10/24 08:15:05',
    },
    {
        id: 4,
        device: 'Đèn 1',
        action: 'off',
        actionLabel: 'Tắt',
        status: 'success',
        statusLabel: 'Thành công',
        user: 'DiTa',
        time: '2026/10/23 18:00:27',
    },
]

const DEVICE_MAP: Record<string, string> = {
    'den-1': 'Đèn 1',
    'den-2': 'Đèn 2',
    quat: 'Quạt thông gió',
}

class MockHistoryService {
    connect() {}

    async fetchLogs(
        params: {
            page?: number
            pageSize?: number
            sortKey?: SortKey | null
            sortDir?: SortDir
            filters?: HistoryFilters
        } = {},
    ): Promise<ActionLogResult> {
        await new Promise((r) => setTimeout(r, 150))

        let items = [...FAKE_LOGS]

        const f = params.filters
        if (f) {
            if (f.device !== 'all') {
                items = items.filter((r) => DEVICE_MAP[f.device] === r.device)
            }
            if (f.id.trim()) {
                items = items.filter((r) => String(r.id).includes(f.id.trim()))
            }
            if (f.action !== 'all') {
                items = items.filter((r) => r.action === f.action)
            }
            if (f.status !== 'all') {
                items = items.filter((r) => r.status === f.status)
            }
            if (f.time.trim()) {
                items = items.filter((r) => r.time.includes(f.time.trim()))
            }
        }

        if (params.sortKey) {
            const key = params.sortKey
            const dir = params.sortDir === 'desc' ? -1 : 1
            items.sort((a, b) => {
                if (key === 'id') return (a.id - b.id) * dir
                // time dạng yyyy/MM/dd HH:mm:ss nên so sánh chuỗi là đúng thứ tự
                return a[key].localeCompare(b[key], 'vi') * dir
            })
        }

        return { items, total: 1000 }
    }
}

export const historyService = new MockHistoryService()
