<template>
    <div
        class="p-margin-mobile md:p-xl flex-1 flex flex-col gap-4 bg-[#F8F9FA] h-[calc(100vh-4rem)] overflow-hidden"
    >
        <!-- Khung bộ lọc tìm kiếm -->
        <SensorFilter
            v-model:filterType="filterType"
            v-model:query="query"
            @clear="clearFilters"
            @apply="handleFilter"
        />

        <!-- Khung chứa Bảng & Phân trang -->
        <div
            class="bg-white rounded-lg border border-gray-100 shadow-[0px_2px_12px_rgba(0,0,0,0.03)] overflow-hidden flex-1 min-h-0 flex flex-col"
        >
            <!-- Bảng dữ liệu -->
            <SensorTable
                :columns="columns"
                :rows="rows"
                :sortKey="sortKey"
                :sortDir="sortDir"
                @sort="toggleSort"
            />

            <!-- Thanh phân trang -->
            <SensorPagination
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
import { ref, computed, onMounted } from 'vue'
import { sensorService } from './sensorService'
import type { SensorRecord, FilterType, SortKey, SortDir } from './sensors'

// Import các Component con
import SensorFilter from './components/SensorFilter.vue'
import SensorTable from './components/SensorTable.vue'
import SensorPagination from './components/SensorPagination.vue'

const filterType = ref<FilterType>('all')
const query = ref('')
const currentPage = ref(1)
const pageSize = ref(5)
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
    console.log(
        'pageSize gửi đi:',
        pageSize.value,
        '| items nhận về:',
        result.items.length,
        '| total:',
        result.total,
    )
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
        sortKey.value = null
        sortDir.value = 'asc'
    }
    currentPage.value = 1
    loadData()
}
</script>
