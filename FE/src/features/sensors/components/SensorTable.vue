<template>
    <div class="overflow-auto flex-1 min-h-0">
        <table class="w-full text-left border-collapse text-[13px] table-fixed">
            <thead>
                <tr
                    class="border-b border-gray-100 bg-[#FAFAFA] text-gray-600 sticky top-0 z-10 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
                >
                    <th
                        v-for="col in columns"
                        :key="col.key"
                        class="py-3 px-4 font-semibold bg-[#FAFAFA] cursor-pointer select-none hover:bg-gray-100 transition-colors"
                        :class="col.width"
                        @click="$emit('sort', col.key)"
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
                    <td class="py-3.5 px-4 font-bold text-gray-900 truncate">
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
                    <td class="py-3.5 px-4 text-gray-700 font-mono truncate">
                        {{ row.time }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import type { SensorRecord, SortKey, SortDir, SensorType } from '../sensors'

const props = defineProps<{
    columns: { key: SortKey; label: string; width: string }[]
    rows: SensorRecord[]
    sortKey: SortKey | null
    sortDir: SortDir
}>()

defineEmits<{
    (e: 'sort', key: SortKey): void
}>()

const sortIcon = (key: SortKey) => {
    if (props.sortKey !== key) return 'unfold_more'
    return props.sortDir === 'asc' ? 'arrow_upward' : 'arrow_downward'
}

const typeBadgeClass = (type: SensorType) => {
    if (type === 'light') return 'bg-amber-50 text-amber-600 border-amber-100'
    if (type === 'humidity') return 'bg-blue-50 text-blue-600 border-blue-100'
    return 'bg-red-50 text-red-600 border-red-100'
}
</script>
