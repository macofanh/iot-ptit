<template>
    <div
        class="bg-white rounded-lg p-4 border border-gray-100 shadow-[0px_2px_8px_rgba(0,0,0,0.02)] flex flex-col gap-3 flex-shrink-0"
    >
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            <!-- Tên thiết bị -->
            <div>
                <label class="block text-[12px] text-gray-600 mb-1 font-medium"
                    >Tên thiết bị</label
                >
                <div class="relative">
                    <select
                        :value="device"
                        @change="
                            $emit(
                                'update:device',
                                ($event.target as HTMLSelectElement).value,
                            )
                        "
                        class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 text-[13px] rounded-md px-3 py-1.5 pr-8 appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                    >
                        <option value="all">Tất cả thiết bị</option>
                        <option value="den-1">Đèn 1</option>
                        <option value="den-2">Đèn 2</option>
                        <option value="quat">Quạt thông gió</option>
                    </select>
                    <span
                        class="material-symbols-outlined text-[18px] text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"
                        >keyboard_arrow_down</span
                    >
                </div>
            </div>

            <!-- Mã thao tác (ID) -->
            <div>
                <label class="block text-[12px] text-gray-600 mb-1 font-medium"
                    >Mã thao tác (ID)</label
                >
                <input
                    :value="id"
                    @input="
                        $emit(
                            'update:id',
                            ($event.target as HTMLInputElement).value,
                        )
                    "
                    type="text"
                    placeholder="VD: 01, OP-102..."
                    class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 placeholder-gray-400 text-[13px] rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                />
            </div>

            <!-- Hành động -->
            <div>
                <label class="block text-[12px] text-gray-600 mb-1 font-medium"
                    >Hành động</label
                >
                <div class="relative">
                    <select
                        :value="action"
                        @change="
                            $emit(
                                'update:action',
                                ($event.target as HTMLSelectElement).value,
                            )
                        "
                        class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 text-[13px] rounded-md px-3 py-1.5 pr-8 appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                    >
                        <option value="all">Tất cả hành động</option>
                        <option value="on">Bật</option>
                        <option value="off">Tắt</option>
                    </select>
                    <span
                        class="material-symbols-outlined text-[18px] text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"
                        >keyboard_arrow_down</span
                    >
                </div>
            </div>

            <!-- Trạng thái -->
            <div>
                <label class="block text-[12px] text-gray-600 mb-1 font-medium"
                    >Trạng thái</label
                >
                <div class="relative">
                    <select
                        :value="status"
                        @change="
                            $emit(
                                'update:status',
                                ($event.target as HTMLSelectElement).value,
                            )
                        "
                        class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 text-[13px] rounded-md px-3 py-1.5 pr-8 appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                    >
                        <option value="all">Tất cả trạng thái</option>
                        <option value="success">Thành công</option>
                        <option value="failed">Thất bại</option>
                        <option value="pending">Đang chờ</option>
                    </select>
                    <span
                        class="material-symbols-outlined text-[18px] text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"
                        >keyboard_arrow_down</span
                    >
                </div>
            </div>

            <!-- Thời gian -->
            <div>
                <label class="block text-[12px] text-gray-600 mb-1 font-medium"
                    >Thời gian</label
                >
                <input
                    :value="time"
                    @input="
                        $emit(
                            'update:time',
                            ($event.target as HTMLInputElement).value,
                        )
                    "
                    type="text"
                    placeholder="VD: 24/10/2024..."
                    class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 placeholder-gray-400 text-[13px] rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                />
            </div>
        </div>

        <!-- Nút bấm hành động -->
        <div
            class="flex items-center justify-end gap-2.5 pt-2 border-t border-gray-100"
        >
            <button
                type="button"
                class="px-4 py-1.5 border border-gray-200 bg-white text-gray-700 text-[13px] font-medium rounded-md hover:bg-gray-50 transition-colors shadow-sm"
                @click="$emit('clear')"
            >
                Xóa bộ lọc
            </button>
            <button
                type="button"
                class="px-4 py-1.5 bg-primary-container text-white text-[13px] font-medium rounded-md hover:opacity-90 transition-opacity shadow-sm flex items-center gap-1.5"
                @click="$emit('apply')"
            >
                <span class="material-symbols-outlined text-[16px]"
                    >search</span
                >
                <span>Áp dụng tìm kiếm</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    device: string
    id: string
    action: string
    status: string
    time: string
}>()

defineEmits<{
    (e: 'update:device', value: string): void
    (e: 'update:id', value: string): void
    (e: 'update:action', value: string): void
    (e: 'update:status', value: string): void
    (e: 'update:time', value: string): void
    (e: 'clear'): void
    (e: 'apply'): void
}>()
</script>
