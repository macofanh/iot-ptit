import type { ProfileInfo } from './profile'
import { setEspConnected } from '@/shared/services/connectionService'

const FAKE_PROFILE: ProfileInfo = {
    fullName: 'Đinh Tuấn Anh',
    phone: '0971231105',
    className: 'IoT Engineer - K65',
    github: 'github.com/macofanh/iot-ptit',
    figma: 'https://www.figma.com/design/epDbVLRfJSdmSIkgFwtlW7/IOT?node-id=0-1&p=f&t=smCgZlf1NjC9xv1R-0',
    apiDocs: 'docs.iot-monitor.io/api',
    avatarUrl:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuAj5jRD9C4IkLMvmHO3yw7kedBg_RZ3DJ869naXBa8a27MiY2AiGwkbYUlKUr4_ydmy9Kbww_HgsrOYnTKn9JuIPtk09PfnkcSdhmJsrNpvyZaXEJQDVVLRbg-57bY9GRKaO6uk5Hw_rHegCZjwKqFp2E6pTWrXpf4_INkd6mJ9dnhODpYO6bvkO6EL-oaWuCjLZdbuHbxgac_DNG_pqWFF_VopCBCdlr8bD_Elum5kY0dgqqOuDrAR',
}

class MockProfileService {
    connect() {}

    async getProfile(): Promise<ProfileInfo> {
        await new Promise((r) => setTimeout(r, 100))
        return { ...FAKE_PROFILE }
    }
}

export const profileService = new MockProfileService()
