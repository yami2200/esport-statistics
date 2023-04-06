<template>
    <div class="card bg-white p-2">
        <Bar
            :options="chartOptions"
            :data="chartData"
        />
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'

import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
export default {
    name: "bar-chart",
    components: { Bar },
    props: {
        chartOptions: {
            type: Object,
            required: true
        },
        chartData: {
            type: Object,
            required: true
        }
    },
}
</script>

<style scoped>

</style>