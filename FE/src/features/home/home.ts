export interface SensorData {
    temperature: number
    humidity: number
    light: number
  }
  
  export interface DeviceState {
    id: 'led1' | 'led2' | 'all'
    name: string
    status: boolean
    topic: string
    icon: string
    subText?: string
  }
  
  export interface StatusResponse {
    device: string
    status: '0' | '1'
    action: 'success' | 'fail'
  }