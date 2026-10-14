<template>
    <div class="p-margin-mobile md:p-lg lg:p-xl max-w-4xl mx-auto w-full">
        <div
            class="bg-surface-container-lowest rounded-xl ambient-shadow p-lg max-w-2xl mx-auto"
        >
            <div class="flex flex-col items-center mb-xl">
                <div class="relative shrink-0 mb-lg">
                    <img
                        :alt="profile.fullName + ' Avatar'"
                        class="w-32 h-32 rounded-full object-cover border-4 border-surface-container-lowest shadow-sm"
                        :src="profile.avatarUrl"
                    />
                </div>
                <h1 class="font-headline-md text-headline-md text-on-surface">
                    Thông tin cá nhân
                </h1>
            </div>
            <div class="space-y-md">
                <div
                    class="flex flex-col sm:flex-row sm:justify-between border-b border-outline-variant/30 pb-sm"
                >
                    <span class="font-semibold text-on-surface-variant"
                        >Họ và tên:</span
                    >
                    <span class="text-on-surface">{{ profile.fullName }}</span>
                </div>
                <div
                    class="flex flex-col sm:flex-row sm:justify-between border-b border-outline-variant/30 pb-sm"
                >
                    <span class="font-semibold text-on-surface-variant"
                        >Số điện thoại:</span
                    >
                    <span class="text-on-surface">{{ profile.phone }}</span>
                </div>
                <div
                    class="flex flex-col sm:flex-row sm:justify-between border-b border-outline-variant/30 pb-sm"
                >
                    <span class="font-semibold text-on-surface-variant"
                        >Lớp:</span
                    >
                    <span class="text-on-surface">{{ profile.className }}</span>
                </div>
                <div
                    class="flex flex-col sm:flex-row sm:justify-between border-b border-outline-variant/30 pb-sm"
                >
                    <span class="font-semibold text-on-surface-variant">
                        GitHub:
                    </span>
                    <a
                        :href="profile.github"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary hover:underline"
                    >
                        {{ profile.github }}
                    </a>
                </div>
                <div
                    class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-outline-variant/30 pb-sm"
                >
                    <span
                        class="font-semibold text-on-surface-variant shrink-0"
                    >
                        Figma:
                    </span>

                    <a
                        :href="profile.figma"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary hover:underline min-w-0 sm:max-w-[75%] break-all sm:text-right"
                    >
                        {{ profile.figma }}
                    </a>
                </div>

                <div
                    class="flex flex-col sm:flex-row sm:justify-between border-b border-outline-variant/30 pb-sm"
                >
                    <span class="font-semibold text-on-surface-variant">
                        API Docs:
                    </span>
                    <a
                        :href="profile.apiDocs"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary hover:underline"
                    >
                        {{ profile.apiDocs }}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { profileService } from './profileService'
import type { ProfileInfo } from './profile'

const profile = reactive<ProfileInfo>({
    fullName: '',
    phone: '',
    className: '',
    github: '',
    figma: '',
    apiDocs: '',
    avatarUrl: '',
})

onMounted(async () => {
    profileService.connect()
    Object.assign(profile, await profileService.getProfile())
})
</script>
