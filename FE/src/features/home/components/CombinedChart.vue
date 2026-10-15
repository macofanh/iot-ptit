<template>
    <div class="w-full h-full flex flex-col min-h-[250px]">
        <div class="flex-1 min-h-0">
            <Line :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Legend,
    type ChartOptions,
} from 'chart.js'

ChartJS.register(
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Legend,
)

const props = defineProps<{
    data: { time: string; temp: number; hum: number; light: number }[]
    filter: string
}>()

const emit = defineEmits<{ (e: 'update:filter', v: string): void }>()

const chartData = computed(() => ({
    labels: props.data.map((d) => d.time),
    datasets: [
        {
            label: 'Nhiệt độ(°C)',
            key: 'temp',
            data: props.data.map((d) => d.temp),
            borderColor: '#ef4444',
            backgroundColor: '#ef4444',
            yAxisID: 'yLeft',
            hidden: !(props.filter === 'all' || props.filter === 'temp'),
        },
        {
            label: 'Độ ẩm(%%%%sđsf)',
            key: 'humidity',
            data: props.data.map((d) => d.hum),
            borderColor: '#3b82f6',
            backgroundColor: '#3b82f6',
            yAxisID: 'yLeft',
            hidden: !(props.filter === 'all' || props.filter === 'humidity'),
        },
        {
            label: 'Ánh sáng(lux)',
            key: 'light',
            data: props.data.map((d) => d.light),
            borderColor: '#eec200',
            backgroundColor: '#eec200',
            yAxisID: 'yRight',
            hidden: !(props.filter === 'all' || props.filter === 'light'),
        },
    ],
}))

const chartOptions = computed<ChartOptions<'line'>>(() => ({
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    interaction: { mode: 'index', intersect: false },
    elements: {
        line: { borderWidth: 2.5, tension: 0.2 },
        point: {
            radius: 3.5,
            hoverRadius: 5,
            borderColor: '#fff',
            borderWidth: 1.5,
        },
    },
    scales: {
        x: {
            grid: { display: false },
            ticks: { font: { size: 10 }, color: '#9ca3af' },
            title: {
                display: true,
                text: 'Thời gian',
                color: '#475569',
                font: { size: 12, weight: 'bold' },
            },
        },
        yLeft: {
            type: 'linear',
            position: 'left',
            min: 0,
            max: 100,
            grid: { color: '#f1f5f9' },
            ticks: { stepSize: 25, font: { size: 10 }, color: '#9ca3af' },
            title: {
                display: true,
                text: 'Nhiệt độ(°C), Độ ẩm(%)',
                color: '#475569',
                font: { size: 12, weight: 'bold' },
            },
        },
        yRight: {
            type: 'linear',
            position: 'right',
            min: 0,
            max: 1000,
            grid: { drawOnChartArea: false },
            ticks: { stepSize: 250, font: { size: 10 }, color: '#9ca3af' },
            title: {
                display: true,
                text: 'Ánh sáng(lux)',
                color: '#475569',
                font: { size: 12, weight: 'bold' },
            },
        },
    },
    plugins: {
        tooltip: { padding: 10 },
        legend: {
            position: 'bottom',
            labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                font: { size: 12 },
            },
            onClick: (_e, item) => {
                const keyMap = ['temp', 'humidity', 'light']
                const key = keyMap[item.datasetIndex ?? 0]
                if (!key) return
                emit('update:filter', props.filter === key ? 'all' : key)
            },
        },
    },
}))
</script>
