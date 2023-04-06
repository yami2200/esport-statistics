<template>
    <div class="card bg-white p-2">
        <Line
                :options="chartOptions"
                :data="chartData"></Line>
    </div>

</template>

<script>
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
export default {
    name: "line-chart",
    components: { Line },
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