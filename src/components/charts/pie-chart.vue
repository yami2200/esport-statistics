<template>
    <div class="card bg-white p-2">
        <Pie
                :options="chartOptions"
                :data="chartData"
        />
    </div>
</template>

<script>
import {Pie} from "vue-chartjs";
import ChartDataLabels from 'chartjs-plugin-datalabels';

import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, ChartDataLabels)
export default {
    name: "pie-chart",
    components: {Pie},
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