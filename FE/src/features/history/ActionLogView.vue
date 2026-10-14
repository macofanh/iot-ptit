<template>
    <div
        class="p-margin-mobile md:p-xl flex-1 flex flex-col gap-4 bg-[#F8F9FA] h-[calc(100vh-4rem)] overflow-hidden"
    >
        <!-- Khung bộ lọc tìm kiếm (Ghim cố định) -->
        <div
            class="bg-white rounded-lg p-4 border border-gray-100 shadow-[0px_2px_8px_rgba(0,0,0,0.02)] flex flex-col gap-3 flex-shrink-0"
        >
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                <!-- Tên thiết bị -->
                <div>
                    <label
                        class="block text-[12px] text-gray-600 mb-1 font-medium"
                        >Tên thiết bị</label
                    >
                    <div class="relative">
                        <select
                            v-model="filters.device"
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
                    <label
                        class="block text-[12px] text-gray-600 mb-1 font-medium"
                        >Mã thao tác (ID)</label
                    >
                    <input
                        v-model="filters.id"
                        type="text"
                        placeholder="VD: 01, OP-102..."
                        class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 placeholder-gray-400 text-[13px] rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                    />
                </div>

                <!-- Hành động -->
                <div>
                    <label
                        class="block text-[12px] text-gray-600 mb-1 font-medium"
                        >Hành động</label
                    >
                    <div class="relative">
                        <select
                            v-model="filters.action"
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
                    <label
                        class="block text-[12px] text-gray-600 mb-1 font-medium"
                        >Trạng thái</label
                    >
                    <div class="relative">
                        <select
                            v-model="filters.status"
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
                    <label
                        class="block text-[12px] text-gray-600 mb-1 font-medium"
                        >Thời gian</label
                    >
                    <input
                        v-model="filters.time"
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
                    @click="clearFilters"
                >
                    Xóa bộ lọc
                </button>
                <button
                    type="button"
                    class="px-4 py-1.5 bg-primary-container text-white text-[13px] font-medium rounded-md hover:opacity-90 transition-opacity shadow-sm flex items-center gap-1.5"
                    @click="handleFilter"
                >
                    <span class="material-symbols-outlined text-[16px]"
                        >search</span
                    >
                    <span>Áp dụng tìm kiếm</span>
                </button>
            </div>
        </div>

        <!-- Khung Bảng & Phân trang -->
        <div
            class="bg-white rounded-lg border border-gray-100 shadow-[0px_2px_12px_rgba(0,0,0,0.03)] overflow-hidden flex-1 min-h-0 flex flex-col"
        >
            <!-- Phần cuộn riêng cho Bảng -->
            <div class="overflow-auto flex-1 min-h-0">
                <table
                    class="w-full text-left border-collapse text-[13px] table-fixed"
                >
                    <thead>
                        <tr
                            class="border-b border-gray-100 bg-[#FAFAFA] text-gray-600 sticky top-0 z-10 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
                        >
                            <th
                                class="py-3 px-4 font-semibold w-[8%] bg-[#FAFAFA] cursor-pointer select-none hover:bg-gray-100 transition-colors"
                                @click="toggleSort('id')"
                            >
                                <div class="flex items-center gap-1">
                                    <span>ID</span>
                                    <span
                                        class="material-symbols-outlined text-[16px]"
                                        :class="
                                            sortKey === 'id'
                                                ? 'text-primary'
                                                : 'text-gray-300'
                                        "
                                        >{{ sortIcon('id') }}</span
                                    >
                                </div>
                            </th>
                            <th
                                class="py-3 px-4 font-semibold w-[18%] bg-[#FAFAFA] cursor-pointer select-none hover:bg-gray-100 transition-colors"
                                @click="toggleSort('device')"
                            >
                                <div class="flex items-center gap-1">
                                    <span>Thiết bị</span>
                                    <span
                                        class="material-symbols-outlined text-[16px]"
                                        :class="
                                            sortKey === 'device'
                                                ? 'text-primary'
                                                : 'text-gray-300'
                                        "
                                        >{{ sortIcon('device') }}</span
                                    >
                                </div>
                            </th>
                            <th
                                class="py-3 px-4 font-semibold w-[14%] bg-[#FAFAFA]"
                            >
                                Hành động
                            </th>
                            <th
                                class="py-3 px-4 font-semibold w-[16%] bg-[#FAFAFA]"
                            >
                                Trạng thái
                            </th>
                            <th
                                class="py-3 px-4 font-semibold w-[20%] bg-[#FAFAFA]"
                            >
                                Người thực hiện
                            </th>
                            <th
                                class="py-3 px-4 font-semibold w-[24%] bg-[#FAFAFA] cursor-pointer select-none hover:bg-gray-100 transition-colors"
                                @click="toggleSort('time')"
                            >
                                <div class="flex items-center gap-1">
                                    <span>Thời gian thao tác</span>
                                    <span
                                        class="material-symbols-outlined text-[16px]"
                                        :class="
                                            sortKey === 'time'
                                                ? 'text-primary'
                                                : 'text-gray-300'
                                        "
                                        >{{ sortIcon('time') }}</span
                                    >
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-gray-800">
                        <tr
                            v-for="row in logs"
                            :key="row.id"
                            class="hover:bg-gray-50/70 transition-colors"
                        >
                            <td
                                class="py-3.5 px-4 font-bold text-gray-900 truncate"
                            >
                                {{ row.id }}
                            </td>
                            <td
                                class="py-3.5 px-4 font-semibold text-gray-700 truncate"
                            >
                                {{ row.device }}
                            </td>
                            <!-- Cột Hành động -->
                            <td class="py-3.5 px-4 truncate">
                                <span
                                    class="inline-flex items-center px-2.5 py-0.5 rounded text-[12px] font-medium border"
                                    :class="actionBadgeClass(row.action)"
                                >
                                    {{ row.actionLabel }}
                                </span>
                            </td>
                            <!-- Cột Trạng thái mới -->
                            <td class="py-3.5 px-4 truncate">
                                <span
                                    class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[12px] font-medium border"
                                    :class="statusBadgeClass(row.status)"
                                >
                                    <span
                                        class="w-1.5 h-1.5 rounded-full"
                                        :class="statusDotClass(row.status)"
                                    />
                                    {{ row.statusLabel }}
                                </span>
                            </td>
                            <td class="py-3.5 px-4 text-gray-800 truncate">
                                <div class="inline-flex items-center gap-1.5">
                                    <span>{{ row.user }}</span>
                                </div>
                            </td>
                            <td
                                class="py-3.5 px-4 text-gray-700 font-mono truncate"
                            >
                                {{ row.time }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Thanh phân trang Footer -->
            <div
                class="border-t border-gray-100 px-4 py-3 flex flex-wrap items-center justify-between gap-3 bg-white text-[13px] flex-shrink-0"
            >
                <div class="flex items-center gap-2 text-gray-600">
                    <span>Hiển thị</span>
                    <select
                        v-model.number="pageSize"
                        class="bg-white border border-gray-200 rounded px-2 py-1 text-gray-800 text-[12px] focus:outline-none focus:border-blue-500"
                        @change="handlePageSizeChange"
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
                    <button
                        type="button"
                        class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                        :disabled="currentPage === 1"
                        @click="goToPage(currentPage - 1)"
                    >
                        Trước
                    </button>

                    <template v-for="(p, index) in visiblePages" :key="index">
                        <span
                            v-if="p === '...'"
                            class="px-1 text-gray-400 select-none"
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
                            @click="goToPage(Number(p))"
                        >
                            {{ p }}
                        </button>
                    </template>

                    <button
                        type="button"
                        class="px-2.5 py-1 text-[13px] rounded transition-colors disabled:text-gray-300 disabled:cursor-not-allowed text-gray-700 hover:bg-gray-100"
                        :disabled="currentPage === totalPages"
                        @click="goToPage(currentPage + 1)"
                    >
                        Tiếp theo
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { historyService } from './historyService'
import type {
    ActionType,
    ActionLog,
    ActionStatus,
    SortKey,
    SortDir,
} from './history'

const filters = reactive({
    device: 'all',
    id: '',
    action: 'all',
    status: 'all',
    time: '',
})

const currentPage = ref(1)
const pageSize = ref(10)
const logs = ref<ActionLog[]>([])
const total = ref(0)
const sortKey = ref<SortKey | null>(null)
const sortDir = ref<SortDir>('asc')

const totalPages = computed(() =>
    Math.max(1, Math.ceil(total.value / pageSize.value)),
)

const toggleSort = (key: SortKey) => {
    if (sortKey.value !== key) {
        sortKey.value = key
        sortDir.value = 'asc'
    } else if (sortDir.value === 'asc') {
        sortDir.value = 'desc'
    } else {
        sortKey.value = null // bấm lần 3: bỏ sắp xếp
        sortDir.value = 'asc'
    }
    currentPage.value = 1
    loadData()
}

const sortIcon = (key: SortKey) => {
    if (sortKey.value !== key) return 'unfold_more'
    return sortDir.value === 'asc' ? 'arrow_upward' : 'arrow_downward'
}

const visiblePages = computed(() => {
    const totalP = totalPages.value
    const current = currentPage.value

    if (totalP <= 5) {
        return Array.from({ length: totalP }, (_, i) => i + 1)
    }

    const pages: (number | string)[] = []
    if (current <= 3) {
        pages.push(1, 2, 3, '...', totalP)
    } else if (current >= totalP - 2) {
        pages.push(1, '...', totalP - 2, totalP - 1, totalP)
    } else {
        pages.push(1, '...', current, '...', totalP)
    }
    return pages
})

const actionBadgeClass = (action: ActionType) => {
    if (action === 'off') return 'bg-gray-100 text-gray-700 border-gray-200'
    return 'bg-blue-50 text-blue-700 border-blue-200'
}

const statusBadgeClass = (status: ActionStatus) => {
    if (status === 'success')
        return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    if (status === 'failed') return 'bg-rose-50 text-rose-700 border-rose-200'
    return 'bg-amber-50 text-amber-700 border-amber-200'
}

const statusDotClass = (status: ActionStatus) => {
    if (status === 'success') return 'bg-emerald-500'
    if (status === 'failed') return 'bg-rose-500'
    return 'bg-amber-500 animate-pulse'
}

const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
        currentPage.value = page
        loadData()
    }
}

const handlePageSizeChange = () => {
    currentPage.value = 1
    loadData()
}

const handleFilter = () => {
    currentPage.value = 1
    loadData()
}

const clearFilters = () => {
    filters.device = 'all'
    filters.id = ''
    filters.action = 'all'
    filters.status = 'all'
    filters.time = ''
    currentPage.value = 1
    loadData()
}

const loadData = async () => {
    const result = await historyService.fetchLogs({
        page: currentPage.value,
        pageSize: pageSize.value,
        sortKey: sortKey.value,
        sortDir: sortDir.value,
    })
    logs.value = result.items
    total.value = result.total
}

onMounted(() => {
    historyService.connect()
    loadData()
})
</script>
