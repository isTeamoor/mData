<template>
    <h1>s-Curve</h1>
    <button @click="show">Show</button>
    <svg id="mySVG" :style="{ 'width': chartWidth + 'px', 'height': chartHeight + 'px' }"></svg>
</template>


<script>
import * as d3 from 'd3';
import { draw } from "@/assets/js/utils"
export default {
    name: "s-Curve",

    data() {
        return {
            chartWidth: 700,
            chartHeight: 300,
            planMonthly: {},
            planCumulat: {},
        }
    },

    methods: {
        show() {
            fetch("http://127.0.0.1:8000/sCurve/planMonthly").then(data => data.json()).then(data => this.planMonthly = data);
            fetch("http://127.0.0.1:8000/sCurve/planCumulat").then(data => data.json()).then(data => this.planCumulat = data);

        }
    },

    watch: {
        planMonthly() {
            draw('#mySVG', this.planMonthly, 'T1', this.chartWidth, this.chartHeight)
        },
        planCumulat() {
            draw('#mySVG', this.planCumulat, 'T2', this.chartWidth, this.chartHeight)
        }
    },
}
</script>


<style scoped>
h1 {
    text-align: center;
}

#mySVG {
    border: 1px solid black;
}
</style>
    