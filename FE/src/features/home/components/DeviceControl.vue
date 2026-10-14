<template>
    <div
        class="bg-surface-container-lowest rounded-xl p-md ambient-shadow flex justify-between items-center card-press"
    >
        <div class="flex items-center gap-sm">
            <div
                class="w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                :class="status ? activeBgClass : 'bg-surface-container'"
            >
                <span
                    class="material-symbols-outlined"
                    :class="
                        status ? activeIconClass : 'text-on-surface-variant'
                    "
                >
                    {{ icon }}
                </span>
            </div>
            <div class="flex flex-col">
                <span
                    class="font-body-lg text-body-lg text-on-surface font-medium"
                    >{{ name }}</span
                >
                <span
                    class="font-label-md text-label-md text-on-surface-variant"
                >
                    {{ status ? 'On' : 'Off' }}
                </span>
            </div>
        </div>

        <button
            type="button"
            :aria-pressed="status"
            class="w-12 h-6 rounded-full relative transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            :class="status ? 'bg-primary-container' : 'bg-surface-variant'"
            @click="$emit('toggle')"
        >
            <span
                class="absolute top-1 left-1 w-4 h-4 rounded-full transition-transform duration-300"
                :class="[
                    status
                        ? 'translate-x-6 bg-on-primary shadow-md'
                        : 'translate-x-0 bg-outline',
                ]"
            ></span>
        </button>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    name: string
    status: boolean
    icon: string
    activeBgClass?: string
    activeIconClass?: string
}>()

defineEmits<{
    (e: 'toggle'): void
}>()
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
