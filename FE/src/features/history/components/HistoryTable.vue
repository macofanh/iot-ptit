<template>
    <div class="overflow-auto flex-1 min-h-0">
        <table class="w-full text-left border-collapse text-[13px] table-fixed">
            <thead>
                <tr
                    class="border-b border-gray-100 bg-[#FAFAFA] text-gray-600 sticky top-0 z-10 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
                >
                    <th
                        v-for="col in columns"
                        :key="col.label"
                        class="py-3 px-4 font-semibold bg-[#FAFAFA]"
                        :class="[
                            col.width,
                            col.sortable
                                ? 'cursor-pointer select-none hover:bg-gray-100 transition-colors'
                                : '',
                        ]"
                        @click="col.sortable && $emit('sort', col.key!)"
                    >
                        <div class="flex items-center gap-1">
                            <span>{{ col.label }}</span>
                            <span
                                v-if="col.sortable"
                                class="material-symbols-outlined text-[16px]"
                                :class="
                                    sortKey === col.key
                                        ? 'text-primary'
                                        : 'text-gray-300'
                                "
                                >{{ sortIcon(col.key!) }}</span
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
                    <td class="py-3.5 px-4 font-bold text-gray-900 truncate">
                        {{ row.id }}
                    </td>
                    <td
                        class="py-3.5 px-4 font-semibold text-gray-700 truncate"
                    >
                        {{ row.device }}
                    </td>
                    <td class="py-3.5 px-4 truncate">
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded text-[12px] font-medium border"
                            :class="actionBadgeClass(row.action)"
                        >
                            {{ row.actionLabel }}
                        </span>
                    </td>
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
                    <td class="py-3.5 px-4 text-gray-700 font-mono truncate">
                        {{ row.time }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import type {
    ActionLog,
    ActionType,
    ActionStatus,
    SortKey,
    SortDir,
} from '../history'

const props = defineProps<{
    logs: ActionLog[]
    sortKey: SortKey | null
    sortDir: SortDir
}>()

defineEmits<{
    (e: 'sort', key: SortKey): void
}>()

const columns: {
    key: SortKey | null
    label: string
    width: string
    sortable: boolean
}[] = [
    { key: 'id', label: 'ID', width: 'w-[8%]', sortable: true },
    { key: 'device', label: 'Thiết bị', width: 'w-[18%]', sortable: true },
    { key: null, label: 'Hành động', width: 'w-[14%]', sortable: false },
    { key: null, label: 'Trạng thái', width: 'w-[16%]', sortable: false },
    { key: null, label: 'Người thực hiện', width: 'w-[20%]', sortable: false },
    {
        key: 'time',
        label: 'Thời gian thao tác',
        width: 'w-[24%]',
        sortable: true,
    },
]

const sortIcon = (key: SortKey) => {
    if (props.sortKey !== key) return 'unfold_more'
    return props.sortDir === 'asc' ? 'arrow_upward' : 'arrow_downward'
}

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
</script>
