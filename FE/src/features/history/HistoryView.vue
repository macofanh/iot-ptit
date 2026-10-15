<template>
    <div
        class="p-margin-mobile md:p-xl flex-1 flex flex-col gap-4 bg-[#F8F9FA] h-[calc(100vh-4rem)] overflow-hidden"
    >
        <!-- Khung bộ lọc tìm kiếm -->
        <HistoryFilter
            v-model:device="filters.device"
            v-model:id="filters.id"
            v-model:action="filters.action"
            v-model:status="filters.status"
            v-model:time="filters.time"
            @clear="clearFilters"
            @apply="handleFilter"
        />

        <!-- Khung chứa Bảng & Phân trang -->
        <div
            class="bg-white rounded-lg border border-gray-100 shadow-[0px_2px_12px_rgba(0,0,0,0.03)] overflow-hidden flex-1 min-h-0 flex flex-col"
        >
            <!-- Bảng dữ liệu -->
            <HistoryTable
                :logs="logs"
                :sortKey="sortKey"
                :sortDir="sortDir"
                @sort="toggleSort"
            />

            <!-- Thanh phân trang -->
            <HistoryPagination
                :pageSize="pageSize"
                :currentPage="currentPage"
                :total="total"
                :totalPages="totalPages"
                :visiblePages="visiblePages"
                @update:pageSize="handlePageSizeChange"
                @changePage="goToPage"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { historyService } from './historyService'
import type { ActionLog, SortKey, SortDir } from './history'

// Import các Component con
import HistoryFilter from './components/HistoryFilter.vue'
import HistoryTable from './components/HistoryTable.vue'
import HistoryPagination from './components/HistoryPagination.vue'

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

// Logic Phân trang
const totalPages = computed(() =>
    Math.max(1, Math.ceil(total.value / pageSize.value)),
)

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

const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
        currentPage.value = page
        loadData()
    }
}

const handlePageSizeChange = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    loadData()
}

// Logic Bộ lọc & Data
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
        filters: { ...filters },
    })
    logs.value = result.items
    total.value = result.total
}

onMounted(() => {
    historyService.connect()
    loadData()
})

const toggleSort = (key: SortKey) => {
    if (sortKey.value !== key) {
        sortKey.value = key
        sortDir.value = 'asc'
    } else if (sortDir.value === 'asc') {
        sortDir.value = 'desc'
    } else {
        sortKey.value = null
        sortDir.value = 'asc'
    }
    currentPage.value = 1
    loadData()
}
</script>
