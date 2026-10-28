import type { ProfileInfo } from './profile'
import Me from '@/assets/images/me.jpeg'

const FAKE_PROFILE: ProfileInfo = {
    fullName: 'Đinh Tuấn Anh',
    phone: '0971231105',
    className: 'IoT Engineer - K65',
    github: 'https://github.com/macofanh/iot-ptit',
    figma: 'https://www.figma.com/design/epDbVLRfJSdmSIkgFwtlW7/IOT?node-id=0-1&p=f&t=smCgZlf1NjC9xv1R-0',
    apiDocs: 'docs.iot-monitor.io/api',
    avatarUrl: Me,
}

class MockProfileService {
    connect() {}

    async getProfile(): Promise<ProfileInfo> {
        await new Promise((r) => setTimeout(r, 100))
        return { ...FAKE_PROFILE }
    }
}

export const profileService = new MockProfileService()
