<template>
    <div
        class="p-margin-mobile md:p-xl flex-1 flex flex-col gap-4 bg-[#F8F9FA] h-[calc(100vh-4rem)] overflow-hidden"
    >
        <!-- Khung bộ lọc tìm kiếm (Ghim cố định) -->
        <div
            class="bg-white rounded-lg p-4 border border-gray-100 shadow-[0px_2px_8px_rgba(0,0,0,0.02)] flex flex-wrap lg:flex-nowrap items-end gap-3 flex-shrink-0"
        >
            <div class="w-full sm:w-60 flex-shrink-0">
                <label
                    class="block text-[12px] text-gray-600 mb-1.5 font-medium"
                    >Tiêu chí lọc</label
                >
                <div class="relative">
                    <select
                        v-model="filterType"
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
                <label
                    class="block text-[12px] text-gray-600 mb-1.5 font-medium"
                    >Giá trị / Thời gian cần tìm</label
                >
                <input
                    v-model="query"
                    type="text"
                    placeholder="Nhập số (VD: 30), mã (#TEMP-01) hoặc ngày giờ (VD: 10:00)"
                    class="w-full bg-[#F1F5F9] border border-[#E2E8F0] text-gray-800 placeholder-gray-400 text-[13px] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
                />
            </div>
            <div
                class="flex items-center gap-2.5 flex-shrink-0 w-full sm:w-auto mt-2 sm:mt-0"
            >
                <button
                    type="button"
                    class="px-4 py-2 border border-gray-200 bg-white text-gray-700 text-[13px] font-medium rounded-md hover:bg-gray-50 transition-colors shadow-sm"
                    @click="clearFilters"
                >
                    Xóa bộ lọc
                </button>
                <button
                    type="button"
                    class="px-4 py-2 bg-primary-container text-white text-[13px] font-medium rounded-md hover:opacity-90 transition-opacity shadow-sm flex items-center gap-1.5"
                    @click="handleFilter"
                >
                    <span class="material-symbols-outlined text-[16px]"
                        >search</span
                    >
                    <span>Áp dụng tìm kiếm</span>
                </button>
            </div>
        </div>

        <!-- Khung chứa Bảng & Phân trang (Tự dãn theo màn hình) -->
        <div
            class="bg-white rounded-lg border border-gray-100 shadow-[0px_2px_12px_rgba(0,0,0,0.03)] overflow-hidden flex-1 min-h-0 flex flex-col"
        >
            <!-- Phần cuộn duy nhất cho Bảng -->
            <div class="overflow-auto flex-1 min-h-0">
                <table
                    class="w-full text-left border-collapse text-[13px] table-fixed"
                >
                    <thead>
                        <tr
                            class="border-b border-gray-100 bg-[#FAFAFA] text-gray-600 sticky top-0 z-10 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
                        >
                            <th
                                v-for="col in columns"
                                :key="col.key"
                                class="py-3 px-4 font-semibold bg-[#FAFAFA] cursor-pointer select-none hover:bg-gray-100 transition-colors"
                                :class="col.width"
                                @click="toggleSort(col.key)"
                            >
                                <div class="flex items-center gap-1">
                                    <span>{{ col.label }}</span>
                                    <span
                                        class="material-symbols-outlined text-[16px]"
                                        :class="
                                            sortKey === col.key
                                                ? 'text-primary'
                                                : 'text-gray-300'
                                        "
                                        >{{ sortIcon(col.key) }}</span
                                    >
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-gray-800">
                        <tr
                            v-for="row in rows"
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
                                {{ row.sensorCode }}
                            </td>
                            <td class="py-3.5 px-4 truncate">
                                <span
                                    class="inline-block px-2.5 py-0.5 rounded text-[12px] font-medium border"
                                    :class="typeBadgeClass(row.type)"
                                    >{{ row.typeLabel }}</span
                                >
                            </td>
                            <td
                                class="py-3.5 px-4 font-mono font-medium text-gray-900 truncate"
                            >
                                {{ row.value }}
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

            <!-- Thanh phân trang Footer (Ghim cố định ở đáy) -->
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
import { ref, computed, onMounted } from 'vue'
import { sensorService } from './sensorService'
import type { SensorRecord, SensorType, SortKey, SortDir } from './sensors'

const filterType = ref<SensorType | 'all'>('all')
const query = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const rows = ref<SensorRecord[]>([])
const total = ref(0)

const sortKey = ref<SortKey | null>(null)
const sortDir = ref<SortDir>('asc')

const columns: { key: SortKey; label: string; width: string }[] = [
    { key: 'id', label: 'ID', width: 'w-[12%]' },
    { key: 'sensorCode', label: 'Mã Sensor', width: 'w-[20%]' },
    { key: 'typeLabel', label: 'Loại cảm biến', width: 'w-[22%]' },
    { key: 'value', label: 'Giá trị', width: 'w-[20%]' },
    { key: 'time', label: 'Thời gian', width: 'w-[26%]' },
]

// Tính tổng số trang
const totalPages = computed(() =>
    Math.max(1, Math.ceil(total.value / pageSize.value)),
)

// Tính danh sách nút trang hiển thị (1, 2, 3, ..., trang cuối)
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

const typeBadgeClass = (type: SensorType) => {
    if (type === 'light') return 'bg-amber-50 text-amber-600 border-amber-100'
    if (type === 'humidity') return 'bg-blue-50 text-blue-600 border-blue-100'
    return 'bg-red-50 text-red-600 border-red-100'
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
    filterType.value = 'all'
    query.value = ''
    currentPage.value = 1
    loadData()
}

const loadData = async () => {
    const result = await sensorService.fetchRecords({
        type: filterType.value,
        query: query.value,
        page: currentPage.value,
        pageSize: pageSize.value,
        sortKey: sortKey.value,
        sortDir: sortDir.value,
    })
    rows.value = result.items
    total.value = result.total
}

onMounted(() => {
    sensorService.connect()
    loadData()
})

const toggleSort = (key: SortKey) => {
    if (sortKey.value !== key) {
        sortKey.value = key
        sortDir.value = 'asc'
    } else if (sortDir.value === 'asc') {
        sortDir.value = 'desc'
    } else {
        sortKey.value = null // lần bấm thứ 3: bỏ sắp xếp
        sortDir.value = 'asc'
    }
    currentPage.value = 1
    loadData()
}

const sortIcon = (key: SortKey) => {
    if (sortKey.value !== key) return 'unfold_more'
    return sortDir.value === 'asc' ? 'arrow_upward' : 'arrow_downward'
}
</script>
