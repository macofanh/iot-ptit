import type { ProfileInfo } from './profile'
import Me from '@/assets/images/me.jpeg'

const FAKE_PROFILE: ProfileInfo = {
    fullName: 'Đinh Tuấn Anh',
    phone: '0971231105',
    className: 'N10 - IoT',
    github: 'https://github.com/macofanh/iot-ptit',
    figma: 'https://www.figma.com/design/epDbVLRfJSdmSIkgFwtlW7/IOT?node-id=0-1&p=f&t=smCgZlf1NjC9xv1R-0',
    apiDocs: 'https://checkable-admirative-mamie.ngrok-free.dev/docs',
    docs: 'https://docs.google.com/document/d/1m02lHgm9pvJgIte1JuFz5QkxbTsoxRCOGuxiaBkdB84/edit?tab=t.0#heading=h.rk6huyr6s1px',
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
