<template>
    <div
        class="bg-surface-container-lowest rounded-xl p-md ambient-shadow flex flex-col gap-sm relative overflow-hidden card-press"
    >
        <div
            class="absolute top-md right-md w-3 h-3 rounded-full animate-pulse"
            :class="badgeBgClass"
        ></div>
        <div class="flex items-center gap-sm text-on-surface-variant">
            <span class="material-symbols-outlined" :class="iconColorClass">{{
                icon
            }}</span>
            <h3 class="font-label-caps text-label-caps uppercase">
                {{ title }}
            </h3>
        </div>
        <div class="flex items-baseline gap-xs mt-sm">
            <span class="font-data-display text-data-display text-on-surface">{{
                displayValue
            }}</span>
            <span class="font-body-md text-body-md text-on-surface-variant">{{
                unit
            }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    title: string
    value: number | string
    unit: string
    icon: string
    iconColorClass: string
    badgeBgClass: string
    decimals?: number
}>()

const displayValue = computed(() => {
    const n = Number(props.value)
    if (Number.isNaN(n)) return props.value
    return n.toFixed(props.decimals ?? 0)
})
</script>

<style scoped>
.ambient-shadow {
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.04);
}
.card-press:active {
    transform: scale(0.98);
    transition: transform 0.1s ease-in-out;
}
</style>
