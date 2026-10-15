export type SensorType = 'light' | 'humidity' | 'temperature'
export type SortKey = 'id' | 'sensorCode' | 'typeLabel' | 'value' | 'time'
export type SortDir = 'asc' | 'desc'
export type FilterType = SensorType | 'all' | 'time'

export interface SensorRecord {
    id: number
    sensorCode: string
    type: SensorType
    typeLabel: string
    value: string
    time: string
}

export interface SensorListResult {
    items: SensorRecord[]
    total: number
    page: number
    pageSize: number
}
