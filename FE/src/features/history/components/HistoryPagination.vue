<template>
    <div
        class="border-t border-gray-100 px-4 py-3 flex flex-wrap items-center justify-between gap-3 bg-white text-[13px] flex-shrink-0"
    >
        <div class="flex items-center gap-2 text-gray-600">
            <span>Hiển thị</span>
            <select
                :value="pageSize"
                @change="
                    $emit(
                        'update:pageSize',
                        Number(($event.target as HTMLSelectElement).value),
                    )
                "
                class="bg-white border border-gray-200 rounded px-2 py-1 text-gray-800 text-[12px] focus:outline-none focus:border-blue-500"
            >
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
            </select>
            <span>bản ghi/trang</span>
            <span class="mx-1 text-gray-300">•</span>
            <span
                >Tổng số
                <strong class="font-bold text-gray-900">{{
                    total.toLocaleString('vi-VN')
                }}</strong>
                kết quả</span
            >
        </div>
        <div class="flex items-center gap-1.5">
            <!-- Về trang đầu -->
            <button
                type="button"
                class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                :disabled="currentPage === 1"
                @click="$emit('changePage', 1)"
            >
                Đầu
            </button>

            <button
                type="button"
                class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                :disabled="currentPage === 1"
                @click="$emit('changePage', currentPage - 1)"
            >
                Trước
            </button>

            <template v-for="(p, index) in visiblePages" :key="index">
                <span v-if="p === '...'" class="px-1 text-gray-400 select-none"
                    >...</span
                >
                <button
                    v-else
                    type="button"
                    class="w-7 h-7 flex items-center justify-center rounded text-[13px] font-medium transition-colors"
                    :class="
                        p === currentPage
                            ? 'bg-primary-container text-white shadow-sm'
                            : 'text-gray-700 hover:bg-gray-100'
                    "
                    @click="$emit('changePage', Number(p))"
                >
                    {{ p }}
                </button>
            </template>

            <button
                type="button"
                class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                :disabled="currentPage === totalPages"
                @click="$emit('changePage', currentPage + 1)"
            >
                Tiếp theo
            </button>

            <!-- Đến trang cuối -->
            <button
                type="button"
                class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                :disabled="currentPage === totalPages"
                @click="$emit('changePage', totalPages)"
            >
                Cuối
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    pageSize: number
    currentPage: number
    total: number
    totalPages: number
    visiblePages: (string | number)[]
}>()

defineEmits<{
    (e: 'update:pageSize', size: number): void
    (e: 'changePage', page: number): void
}>()
</script>
