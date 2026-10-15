export type ActionType = 'on' | 'off'
export type ActionStatus = 'success' | 'failed' | 'pending'
export type SortKey = 'id' | 'device' | 'time'
export type SortDir = 'asc' | 'desc'

export interface ActionLog {
    id: number
    device: string
    action: ActionType
    actionLabel: string
    status: ActionStatus
    statusLabel: string
    user: string
    time: string
}

export interface ActionLogResult {
    items: ActionLog[]
    total: number
}

export interface HistoryFilters {
    device: string
    id: string
    action: string
    status: string
    time: string
}
