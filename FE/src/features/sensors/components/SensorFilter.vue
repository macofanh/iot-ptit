<template>
    <div
        class="bg-white rounded-lg p-4 border border-gray-100 shadow-[0px_2px_8px_rgba(0,0,0,0.02)] flex flex-wrap lg:flex-nowrap items-end gap-3 flex-shrink-0"
    >
        <div class="w-full sm:w-60 flex-shrink-0">
            <label class="block text-[12px] text-gray-600 mb-1.5 font-medium"
                >Tiêu chí lọc</label
            >
            <div class="relative">
                <select
                    :value="filterType"
                    @input="
                        $emit(
                            'update:filterType',
                            ($event.target as HTMLSelectElement).value,
                        )
                    "
                    class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 text-[13px] rounded-md px-3 py-2 pr-8 appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                >
                    <option value="all">Tất cả cảm biến</option>
                    <option value="light">Ánh sáng</option>
                    <option value="humidity">Độ ẩm</option>
                    <option value="temperature">Nhiệt độ</option>
                    <option value="time">Thời gian</option>
                </select>
                <span
                    class="material-symbols-outlined text-[18px] text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"
                    >keyboard_arrow_down</span
                >
            </div>
        </div>
        <div class="w-full flex-1 min-w-[240px]">
            <label class="block text-[12px] text-gray-600 mb-1.5 font-medium"
                >Giá trị / Thời gian cần tìm</label
            >
            <input
                :value="query"
                @input="
                    $emit(
                        'update:query',
                        ($event.target as HTMLInputElement).value,
                    )
                "
                @keyup.enter="$emit('apply')"
                type="text"
                placeholder="Nhập số (VD: 30), mã (#TEMP-01) hoặc ngày giờ (VD: 27/10/2026 hoặc 09:41)"
                class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 placeholder-gray-400 text-[13px] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
            />
        </div>
        <div
            class="flex items-center gap-2.5 flex-shrink-0 w-full sm:w-auto mt-2 sm:mt-0"
        >
            <button
                type="button"
                class="cursor-pointer px-4 py-2 border border-gray-200 bg-white text-gray-700 text-[13px] font-medium rounded-md hover:bg-gray-50 transition-colors shadow-sm"
                @click="$emit('clear')"
            >
                Xóa bộ lọc
            </button>
            <button
                type="button"
                class="cursor-pointer px-4 py-2 bg-primary-container text-white text-[13px] font-medium rounded-md hover:opacity-90 transition-opacity shadow-sm flex items-center gap-1.5"
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
import type { FilterType } from '../sensors'

defineProps<{
    filterType: FilterType
    query: string
}>()

defineEmits<{
    (e: 'update:filterType', value: string): void
    (e: 'update:query', value: string): void
    (e: 'clear'): void
    (e: 'apply'): void
}>()
</script>
