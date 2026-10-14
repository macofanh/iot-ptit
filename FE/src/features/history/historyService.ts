import type { ActionLog, ActionLogResult, SortKey, SortDir } from './history'

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

class MockHistoryService {
    connect() {}

    async fetchLogs(
        params: {
            page?: number
            pageSize?: number
            sortKey?: SortKey | null
            sortDir?: SortDir
        } = {},
    ): Promise<ActionLogResult> {
        await new Promise((r) => setTimeout(r, 150))

        const items = [...FAKE_LOGS]

        if (params.sortKey) {
            const key = params.sortKey
            const dir = params.sortDir === 'desc' ? -1 : 1
            items.sort((a, b) => {
                if (key === 'id') return (a.id - b.id) * dir
                // time dạng yyyy/MM/dd HH:mm:ss nên so sánh chuỗi là đúng thứ tự
                return a[key].localeCompare(b[key], 'vi') * dir
            })
        }

        return { items, total: 124 }
    }
}

export const historyService = new MockHistoryService()
